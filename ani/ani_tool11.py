# -*- coding: utf-8 -*-
import json

# ani_tool10: 删除动画中的 'timeline' 键

ani_list = ['lwdao.animation.json']

def remove_bones_key(animation_data):
    """从动画中删除 'bones' 键"""
    if 'animations' in animation_data:
        for animation_name, animation in animation_data['animations'].items():
            if 'timeline' in animation:
                del animation['timeline']
    return animation_data

# Process each animation file in ani_list
for ani_file in ani_list:
    try:
        # Load the animation JSON file
        with open(ani_file, 'r', encoding='utf-8') as f:
            animation_data = json.load(f)

        # Remove 'bones' key
        modified_animation = remove_bones_key(animation_data)

        # Save the modified animation to a new file
        output_file = 'notimeline_' + ani_file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(modified_animation, f, indent=4, ensure_ascii=False)

        print(f"'bones' key removed from {ani_file} and saved to {output_file}")

    except FileNotFoundError:
        print(f"File {ani_file} not found, skipping.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {ani_file}, skipping.")
    except Exception as e:
        print(f"Error processing {ani_file}: {e}")

print("All animations processed.")