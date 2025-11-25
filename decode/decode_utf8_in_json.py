import json
import os


def convert_json_encoding(input_file, output_file):
    """
    读取包含 Unicode 转义符(如 \\u9aa8)的 JSON 文件，
    并将其转换为可读字符保存。
    """

    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"错误: 找不到文件 '{input_file}'")
        return

    try:
        # 1. 读取原始文件
        # Python 的 json.load 会自动将 \\uXXXX 解析为内存中的正常字符
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 2. 保存为新文件
        # 关键参数: ensure_ascii=False (允许输出非 ASCII 字符)
        # indent=4 用于美化输出，使其更易读
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"转换成功！已保存为: {output_file}")

    except json.JSONDecodeError:
        print("错误: 文件内容不是有效的 JSON 格式。")
    except Exception as e:
        print(f"发生未知错误: {e}")


# --- 在这里修改文件名 ---
source_file = 'data.json'  # 你的原始文件名
target_file = 'readable.json'  # 你想保存的文件名
# -----------------------

convert_json_encoding(source_file, target_file)