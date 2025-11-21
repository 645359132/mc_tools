# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

# anitool3：克隆骨骼

file_names = ["lwqiang.animation.json"]  # 可以恢复完整列表

def safe_write_json(data, filename):
    """安全写入 JSON 文件的跨平台方案"""
    file_path = Path(filename).absolute()
    file_dir = file_path.parent

    try:
        # 在目标目录创建临时文件
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=str(file_dir),  # 关键修改：确保临时文件和目标文件在同一个目录
            delete=False,
            suffix=".tmp"
        ) as tmp_file:
            json.dump(data, tmp_file, ensure_ascii=False, indent=4)
            tmp_file.write('\n')
            tmp_name = tmp_file.name

        # 原子替换操作（同一磁盘分区）
        os.replace(tmp_name, str(file_path))
        print(f"文件 {file_path.name} 更新成功")

    except Exception as e:
        print(f"写入失败: {type(e).__name__} - {e}")
        if Path(tmp_name).exists():
            Path(tmp_name).unlink()
        raise

# 读取部分保持不变（建议保留之前的异常处理）
for file_name in file_names:
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"文件读取失败: {type(e).__name__} - {e}")
        exit()

    # 数据修改逻辑：保留原始骨骼，添加克隆，移除小写版本的首字母大小写区分骨骼
    for anim in data["animations"].values():
        new_bones = anim["bones"].copy()  # 复制所有原始骨骼，保留它们
        for bone, frames in list(anim["bones"].items()):  # 使用 list() 以避免在遍历时修改
            print(f"正在处理 {bone} 骨骼")
            # 映射关系字典
            bone_mapping = {
                "Root_Up": "rootUp",
                "Root_Down": "rootDown",
                "Root_Mid_covered": "rootMidCovered",
                "Root_Mid": "rootMid",
                "Root_covered": "rootCovered",
                "Waist_covered": "waistCovered",
                "Body_Down_Layer": "bodyDownLayer",
                "Body_Down_Mid": "bodyDownMid",
                "Body_Mid": "bodyMid",
                "Body_Mid_Layer": "bodyMidLayer",
                "Body_Mid_Mid": "bodyMidMid",
                "Body_Up": "bodyUp",
                "Body_Up_Layer": "bodyUpLayer",
                "Left_Arm_Up": "leftArmUp",
                "LeftArm_Layer": "leftArmLayer",
                "Left_Arm_Mid": "leftArmMid",
                "Left_Arm_Down_Layer": "leftArmDownLayer",
                "LeftItem_covered": "leftItemCovered",
                "Right_Arm_Up": "rightArmUp",
                "RightArm_Layer": "rightArmLayer",
                "Right_Arm_Mid": "rightArmMid",
                "Right_Arm_Down_Layer": "rightArmDownLayer",
                "RightItem_covered": "rightItemCovered",
                "Left_Arm_Down": "leftArmDown",
                "Right_Arm_Down": "rightArmDown",
                "Left_Leg_Down": "leftLegDown",
                "Right_Leg_Down": "rightLegDown",
                "Body_Down": "bodyDown",
                # 首字母大小写区分的骨骼（只留下大写的）
                # "Cape": "cape",
                # "Legs": "legs",
                # "Root": "root",
                # "Body": "body",
                # "Head": "head",
                # "LeftArm": "leftArm",
                # "RightArm": "rightArm",
                # "LeftLeg": "leftLeg",
                # "RightLeg": "rightLeg",

            }
            for origin_bone, new_bone in bone_mapping.items():
                if origin_bone in anim["bones"]:
                    if new_bone == origin_bone.lower():  # 只有首字母大小写区分的，移除小写版本
                        print(f"移除小写版本 {new_bone}，保留大写 {origin_bone}")
                        new_bones.pop(new_bone, None)  # 移除小写版本（如果存在）
                    else:  # 克隆
                        print(f"克隆 {origin_bone} -> {new_bone}")
                        new_bones[new_bone] = anim["bones"][origin_bone]  # 添加克隆的骨骼

        anim["bones"] = new_bones  # 更新骨骼数据（包含原始 + 克隆，移除指定小写版本）

    # 调用安全的写入方法
    safe_write_json(data, file_name)