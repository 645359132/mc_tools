# -*- coding: utf-8 -*-
import json
# ani_tool9: 保留列表中的骨骼的动画

ani_list = ['zheshan_open_and_close.json']

bones_to_reserve = ["shangu2", "shangu3", "shangu4", "shangu5", "shangu6", "shangu7", "shangu8", "shangu9", "shangu10", "shangu11", "shangu12", "shangu13", "shangu14", "shangu15", "shangu16", "shangu17", "shangu18", "shangu19", "shangu20", "shangu21", "shangu22", "shangu23", "shangu24", "shangu25", "shangu26", "shangu27", "shangu28", "shangu29", "shangu30", "shangu31", "shangu32",
                   "shanmian1", "shanmian2", "shanmian3", "shanmian4", "shanmian5", "shanmian6", "shanmian7", "shanmian8", "shanmian9", "shanmian10", "shanmian11", "shanmian12", "shanmian13", "shanmian14", "shanmian15", "shanmian16", "shanmian17", "shanmian18", "shanmian19", "shanmian20", "shanmian21", "shanmian22", "shanmian23", "shanmian24", "shanmian25", "shanmian26", "shanmian27",
                   "shanmian28", "shanmian29", "shanmian30", "shanmian31", "shanmian32"
                   ]

def keep_bones_animation(animation_data, bones_to_reserve):
    """从动画中保留指定的骨骼，移除其他骨骼"""
    if 'animations' in animation_data:
        for animation_name, animation in animation_data['animations'].items():
            if 'bones' in animation:
                # 创建新字典，只保留指定的骨骼
                reserved_bones = {bone: frames for bone, frames in animation['bones'].items() if bone in bones_to_reserve}
                animation['bones'] = reserved_bones
    return animation_data

# Process each animation file in ani_list
for ani_file in ani_list:
    try:
        # Load the animation JSON file
        with open(ani_file, 'r', encoding='utf-8') as f:
            animation_data = json.load(f)

        # Keep specified bones
        modified_animation = keep_bones_animation(animation_data, bones_to_reserve)

        # Save the modified animation to a new file
        output_file = 'reserved_' + ani_file  # 更改为 'reserved_' 以反映保留功能
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(modified_animation, f, indent=4, ensure_ascii=False)

        print(f"Bones kept from {ani_file} and saved to {output_file}")

    except FileNotFoundError:
        print(f"File {ani_file} not found, skipping.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {ani_file}, skipping.")
    except Exception as e:
        print(f"Error processing {ani_file}: {e}")

print("All animations processed.")