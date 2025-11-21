# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

# file_names = ["lw_broadblade_long.animation.json", "lw_zhongkuodao.animation.json", "lwdao.animation.json", "lw_jian.animation.json",
#               "lwqiang.animation.json", "lwtaijitu.animation.json", "lwzheshan.animation.json"]
file_names = ["lwqiang.animation.json"]


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

    # 数据修改逻辑保持不变
    for anim in data["animations"].values():
        new_bones = anim["bones"].copy()  # 先复制原始数据
        bone_mapping = {
            'rootUp': 'Root_Up',
            'rootDown': 'Root_Down',
            'rootMidCovered': 'Root_Mid_Covered',
            'rootMid': 'Root_Mid',
            'rootCovered': 'Root_covered',
            'waistCovered': 'Waist_covered',
            'bodyDownLayer': 'Body_Down_Layer',
            'bodyDownMid': 'Body_Down_Mid',
            'bodyMid': 'Body_Mid',
            'bodyMidLayer': 'Body_Mid_Layer',
            'bodyMidMid': 'Body_Mid_Mid',
            'bodyUp': 'Body_Up',
            'bodyUpLayer': 'Body_Up_Layer',
            'leftArmUp': 'Left_Arm_Up',
            'leftArmLayer': 'LeftArm_Layer',
            'leftArmMid': 'Left_Arm_Mid',
            'leftArmDownLayer': 'Left_Arm_Down_Layer',
            'leftItemCovered': 'LeftItem_covered',
            'rightArmUp': 'Right_Arm_Up',
            'rightArmLayer': 'RightArm_Layer',
            'rightArmMid': 'Right_Arm_Mid',
            'rightArmDownLayer': 'Right_Arm_Down_Layer',
            'rightItemCovered': 'RightItem_covered',
            # 'cape': 'Cape',
            # 'legs': 'Legs',
            'leftLegUp': 'Left_Leg_Up',
            'leftLegLayer': 'LeftLeg_Layer',
            'leftLegMid': 'Left_Leg_Mid',
            'leftLegDownLayer': 'Left_Leg_Down_Layer',
            'rightLegUp': 'Right_Leg_Up',
            'rightLegLayer': 'RightLeg_Layer',
            'rightLegMid': 'Right_Leg_Mid',
            'rightLegDownLayer': 'Right_Leg_Down_Layer',
            # 'root': 'Root',
            # 'body': 'Body',
            # 'head': 'Head',
            # 'leftArm': 'LeftArm',
            # 'rightArm': 'RightArm',
            # 'leftLeg': 'LeftLeg',
            # 'rightLeg': 'RightLeg',
            'leftArmDown': 'Left_Arm_Down',
            'rightArmDown': 'Right_Arm_Down',
            'leftLegDown': 'Left_Leg_Down',
            'rightLegDown': 'Right_Leg_Down',
            'bodyDown': 'Body_Down'
        }
        # 注释掉的行是因为发现编译动画不区分大小写，所以不需要修改骨骼名称

        # 遍历映射关系添加新骨骼
        for origin_bone, new_bone in bone_mapping.items():
            if origin_bone in anim["bones"]:
                print(f"克隆 {origin_bone} -> {new_bone}")
                new_bones[new_bone] = anim["bones"][origin_bone]  # 复制帧数据

        anim["bones"] = new_bones  # 合并新旧骨骼数据

    # 调用安全的写入方法
    safe_write_json(data, file_name)