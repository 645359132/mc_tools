import os
import re
import argparse
import shutil
import tempfile

# 正则表达式，用于匹配一个或多个连续的 \xHH 格式的字节序列
BYTE_SEQUENCE_PATTERN = re.compile(r'(\\x[0-9a-fA-F]{2})+')


def decode_match_to_utf8(match: re.Match) -> str:
    """
    这是一个传递给 re.sub 的回调函数。
    它会尝试将匹配到的字节序列字符串解码为UTF-8文本。
    """
    original_str = match.group(0)
    hex_str = original_str.replace('\\x', '')

    try:
        byte_seq = bytes.fromhex(hex_str)
        decoded_str = byte_seq.decode('utf-8')
        # 返回解码后的干净字符串，不需要像之前那样为了放入代码而转义
        return decoded_str
    except (ValueError, UnicodeDecodeError):
        print(f"  [!] 警告：无法解码序列 '{original_str}'，已跳过。")
        return original_str


def process_file(file_path: str):
    """
    处理单个Python文件。
    采用安全的写入方式：先写入临时文件，成功后再替换原文件。
    """
    print(f"--- 正在处理文件: {file_path} ---")

    try:
        # 1. 读取文件内容
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # 2. 使用正则表达式查找并替换所有匹配的序列
        new_content = BYTE_SEQUENCE_PATTERN.sub(decode_match_to_utf8, content)

        # 3. 如果内容有变化，则执行安全的写回操作
        if new_content != content:
            print(f"  [+] 检测到可转换的字符串，正在更新文件...")

            # 创建一个与原文件在同一目录下的临时文件
            # 这能确保 `shutil.move` 在大多数情况下是原子操作
            fd, temp_path = tempfile.mkstemp(suffix='.tmp', dir=os.path.dirname(file_path), text=True)

            with os.fdopen(fd, 'w', encoding='utf-8') as temp_f:
                temp_f.write(new_content)

            # 使用 shutil.move 替换原文件，这比 os.rename 更具可移植性和安全性
            shutil.move(temp_path, file_path)

            print(f"  [*] 文件 '{file_path}' 更新成功，没有留下备份文件。")
        else:
            print(f"  [*] 文件中未找到需要转换的字符串。")

    except FileNotFoundError:
        print(f"  [!] 错误: 文件未找到 '{file_path}'")
    except Exception as e:
        print(f"  [!] 处理文件 '{file_path}' 时发生未知错误: {e}")
        # 如果出错，确保删除可能已创建的临时文件
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)


def main():
    parser = argparse.ArgumentParser(
        description="一个用于将 .py 文件中 UTF-8 字节序列字符串转换为可读中文字符的工具 (直接修改，不留备份)。",
        epilog="示例: python decode_utf8_in_py.py ./my_project"
    )
    parser.add_argument(
        "path",
        help="要处理的文件夹路径或单个.py文件路径。"
    )
    args = parser.parse_args()

    target_path = args.path

    if not os.path.exists(target_path):
        print(f"错误：路径 '{target_path}' 不存在。")
        return

    if os.path.isfile(target_path):
        if target_path.endswith('.py'):
            process_file(target_path)
        else:
            print(f"错误：目标是一个文件，但不是 .py 文件。")
    elif os.path.isdir(target_path):
        print(f"开始扫描目录: {target_path}")
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    process_file(file_path)
    else:
        print(f"错误：路径 '{target_path}' 不是一个有效的文件或目录。")

    print("\n处理完成。")


if __name__ == "__main__":
    main()