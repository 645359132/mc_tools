# -*- coding: utf-8 -*-
import json

# ani_tool6.py 更改动画的item骨骼位置和旋转到rightitem下
bone_name_list = ['Root_Up', 'Root_Down', 'Root_Mid_covered', 'Root_Mid', 'Root_covered', 'root',
                  'Waist', 'body', 'Body_Down', 'Body_Mid', 'Body_Up', 'Right_Arm_Up', 'RightArm',
                  'Right_Arm_Down']

def str_to_num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return 0

def convert_static_to_dict(prop_dict):
    """将静态列表转换为字典格式 {'0.0': value}"""
    if isinstance(prop_dict, list):
        return {'0.0': prop_dict}
    return prop_dict

def interpolate_keyframe(key_frames, key_frame_time, prop='position'):
    """插值函数，假设值是列表"""
    positive_gap = 100.0
    next_frame = None
    negative_gap = -100.0
    last_frame = None
    for kf_time in key_frames:
        num_kf_time = str_to_num(kf_time)
        num_time = str_to_num(key_frame_time)
        if num_kf_time < num_time:
            gap = num_time - num_kf_time
            if gap > negative_gap:
                negative_gap = gap
                last_frame = kf_time
        else:
            gap = num_kf_time - num_time
            if gap < positive_gap:
                positive_gap = gap
                next_frame = kf_time
    if next_frame is not None and last_frame is not None:
        time_from_last_to_next = str_to_num(next_frame) - str_to_num(last_frame)
        time_from_last_to_now = str_to_num(key_frame_time) - str_to_num(last_frame)
        last_val = key_frames[last_frame]  # 假设是列表
        next_val = key_frames[next_frame]  # 假设是列表
        val_now = []
        if time_from_last_to_next != 0:
            factor = time_from_last_to_now / time_from_last_to_next
            for i in range(3):
                val_now.append(last_val[i] + (next_val[i] - last_val[i]) * factor)
        else:
            # If division by zero, use average
            for i in range(3):
                val_now.append((last_val[i] + next_val[i]) / 2)
        return val_now
    return [0, 0, 0]

def adjust_item_animation(animation_data):
    if 'animations' in animation_data:
        for animation_name, animation in animation_data['animations'].items():
            if 'bones' in animation and 'item' in animation['bones']:
                item_key_frames = animation['bones']['item']
                key_frames_map = {}
                key_frames_time_list = []
                for bone_name in bone_name_list:
                    if bone_name in animation['bones']:
                        key_frames_map[bone_name] = animation['bones'][bone_name]

                # 转换item的静态属性为字典
                if 'position' in item_key_frames:
                    item_key_frames['position'] = convert_static_to_dict(item_key_frames['position'])
                if 'rotation' in item_key_frames:
                    item_key_frames['rotation'] = convert_static_to_dict(item_key_frames['rotation'])

                # 转换所有骨骼的静态属性为字典
                for bone_name in key_frames_map:
                    bone = key_frames_map[bone_name]
                    if 'position' in bone:
                        bone['position'] = convert_static_to_dict(bone['position'])
                    if 'rotation' in bone:
                        bone['rotation'] = convert_static_to_dict(bone['rotation'])

                # 收集时间点
                for bone_name, key_frames in item_key_frames.items():
                    if 'position' in key_frames:
                        for key_frame_time in key_frames['position']:
                            if key_frame_time not in key_frames_time_list:
                                key_frames_time_list.append(key_frame_time)
                    if 'rotation' in key_frames:
                        for key_frame_time in key_frames['rotation']:
                            if key_frame_time not in key_frames_time_list:
                                key_frames_time_list.append(key_frame_time)

                key_frames_time_list.sort()

                # 插值item的position和rotation到所有时间点
                if 'position' in item_key_frames:
                    for key_frame_time in key_frames_time_list:
                        if key_frame_time not in item_key_frames['position']:
                            item_key_frames['position'][key_frame_time] = interpolate_keyframe(item_key_frames['position'], key_frame_time, 'position')

                if 'rotation' in item_key_frames:
                    for key_frame_time in key_frames_time_list:
                        if key_frame_time not in item_key_frames['rotation']:
                            item_key_frames['rotation'][key_frame_time] = interpolate_keyframe(item_key_frames['rotation'], key_frame_time, 'rotation')

                key_frames_time_list = [key_frame_time for key_frame_time in item_key_frames['position']]
                key_frames_time_list.sort()

                # 插值所有骨骼的position到item position的时间点
                for bone_name, key_frames in key_frames_map.items():
                    if 'position' in key_frames:
                        for key_frame_time in key_frames_time_list:
                            if key_frame_time not in key_frames['position']:
                                key_frames['position'][key_frame_time] = interpolate_keyframe(key_frames['position'], key_frame_time, 'position')

                    if 'rotation' in key_frames:
                        for key_frame_time in key_frames_time_list:
                            if key_frame_time not in key_frames['rotation']:
                                key_frames['rotation'][key_frame_time] = interpolate_keyframe(key_frames['rotation'], key_frame_time, 'rotation')

                # 现在减去变换，假设所有值都是列表
                for bone_name, key_frames in key_frames_map.items():
                    if 'position' in key_frames:
                        for pos_key_frame_time in item_key_frames['position']:
                            bone_pos_val = key_frames['position'].get(pos_key_frame_time, [0, 0, 0])
                            for i in range(3):
                                item_key_frames['position'][pos_key_frame_time][i] += bone_pos_val[i]

                    if 'rotation' in key_frames:
                        for rot_key_frame_time in item_key_frames['rotation']:
                            bone_rot_val = key_frames['rotation'].get(rot_key_frame_time, [0, 0, 0])
                            for i in range(3):
                                item_key_frames['rotation'][rot_key_frame_time][i] += bone_rot_val[i]

    return animation_data

# Load the animation JSON file
# Replace 'input_animation.json' with your animation file path
with open('simplified_animation.json', 'r', encoding='utf-8') as f:
    animation_data = json.load(f)

# Adjust the animation
adjusted_animation = adjust_item_animation(animation_data)

# Save the adjusted animation to a new file
# Replace 'output_animation.json' with your desired output path
with open('output_animation.json', 'w', encoding='utf-8') as f:
    json.dump(adjusted_animation, f, indent=4, ensure_ascii=False)

print("Animation adjusted and saved to 'output_animation.json'")