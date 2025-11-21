# -*- coding: utf-8 -*-
import json
# ani_tool8: 删除列表中指定的骨骼的动画

# ani_list = ['lw_broadblade_long.animation.json', 'lw_jian.animation.json',
#             'lw_zhongkuodao.animation.json', 'lwdao.animation.json',
#             'lwqiang.animation.json', 'lwtaijitu.animation.json',
#             'lwzheshan.animation.json']
ani_list = ['lwdao.animation.json']

# bones_to_remove = ['item', 'effecta', 'effectb', 'effect', 'effect_longweapon',
#                    'effectMid_longweapon', 'effecta_longweapon', 'effectb_longweapon',
#                    'effect_longweapon_vertical', 'effectMid_longweapon_vertical',
#                    'effecta_longweapon_vertical', 'effectb_longweapon_vertical',
#                    'rootMid', 'rootMidcovered', 'rootDown',
#                    'bodyDown', 'bodyMid', 'bodyUp', 'leftArm', 'leftArmDown',
#                    'rightArm', 'rightArmDown', 'leftLeg', 'leftLegDown',
#                    'rightLeg', 'rightLegDown']
bones_to_remove = ["guang", "mid", "shangu2", "shangu3", "shangu4", "shangu5", "shangu6", "shangu7", "shangu8", "shangu9", "shangu10", "shangu11", "shangu12", "shangu13", "shangu14", "shangu15", "shangu16", "shangu17", "shangu18", "shangu19", "shangu20", "shangu21", "shangu22", "shangu23", "shangu24", "shangu25", "shangu26", "shangu27", "shangu28", "shangu29", "shangu30", "shangu31", "shangu32",
                   "shanmian1", "shanmian2", "shanmian3", "shanmian4", "shanmian5", "shanmian6", "shanmian7", "shanmian8", "shanmian9", "shanmian10", "shanmian11", "shanmian12", "shanmian13", "shanmian14", "shanmian15", "shanmian16", "shanmian17", "shanmian18", "shanmian19", "shanmian20", "shanmian21", "shanmian22", "shanmian23", "shanmian24", "shanmian25", "shanmian26", "shanmian27",
                   "shanmian28", "shanmian29", "shanmian30", "shanmian31", "shanmian32", 'dao', "jian", "qiao", "item", "lisheng_effecta", "lisheng_effectb",
                   "effect2", "effecta2", "effectb2",
                   "effecta", "effectb"
                   ]

def remove_bones_animation(animation_data, bones_to_remove):
    """从动画中移除指定的骨骼"""
    if 'animations' in animation_data:
        for animation_name, animation in animation_data['animations'].items():
            if 'bones' in animation:
                for bone in bones_to_remove:
                    if bone in animation['bones']:
                        del animation['bones'][bone]
    return animation_data

# Process each animation file in ani_list
for ani_file in ani_list:
    try:
        # Load the animation JSON file
        with open(ani_file, 'r', encoding='utf-8') as f:
            animation_data = json.load(f)

        # Remove specified bones
        modified_animation = remove_bones_animation(animation_data, bones_to_remove)

        # Save the modified animation to a new file
        output_file = 'removed_' + ani_file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(modified_animation, f, indent=4, ensure_ascii=False)

        print(f"Bones removed from {ani_file} and saved to {output_file}")

    except FileNotFoundError:
        print(f"File {ani_file} not found, skipping.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {ani_file}, skipping.")
    except Exception as e:
        print(f"Error processing {ani_file}: {e}")

print("All animations processed.")