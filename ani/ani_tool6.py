# -*- coding: utf-8 -*-
import json

def simplify_keyframes(animation_data):
    """将 position 和 rotation 中含有 'post' 的字典关键帧替换为 'post' 的值"""
    if 'animations' in animation_data:
        for animation_name, animation in animation_data['animations'].items():
            if 'bones' in animation:
                for bone_name, bone in animation['bones'].items():
                    for prop in ['position', 'rotation']:
                        if prop in bone:
                            prop_dict = bone[prop]
                            if isinstance(prop_dict, dict):
                                for key, value in list(prop_dict.items()):
                                    if isinstance(value, dict) and 'post' in value:
                                        prop_dict[key] = value['post']
    return animation_data

# Load the animation JSON file
# Replace 'lwqiang.animation.json' with your animation file path
with open('lwqiang.animation.json', 'r', encoding='utf-8') as f:
    animation_data = json.load(f)

# Simplify keyframes
simplified_animation = simplify_keyframes(animation_data)

# Save the simplified animation to a new file
# Replace 'simplified_animation.json' with your desired output path
with open('simplified_animation.json', 'w', encoding='utf-8') as f:
    json.dump(simplified_animation, f, indent=4, ensure_ascii=False)

print("Animation simplified and saved to 'simplified_animation.json'")