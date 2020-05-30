#!/usr/bin/env python3

import json
import os

name = pwd.getpwuid( os.getuid() ).pw_name
user_path = '/home/%s/'%name

#TODO: get file path dynamically
if not os.stat('%s/Documents/Python/Yoga_Bot/Library/yoga_poses.json'%(user_path)).st_size == 0:
    with open('%s/Documents/Python/Yoga_Bot/Library/yoga_poses.json'%(user_path),'r') as fp:
        yoga_dict = json.load(fp)
else:
    yoga_dict = {}


# Name - Key of the nested dict
key1 = input('Enter pose name: ')

keys = []
vals = []
# Focus Area
keys.append('Focus')
user_inp = input('Enter focus area: ')
vals.append(user_inp)

# Img Name
keys.append('Image')
user_inp = input('Enter image name: ')
vals.append(user_inp)

# Time
#   easy, med, hard
keys.append('Time')
user_inp = input('Enter time: ')
vals.append(user_inp)

# Difficulty
keys.append('Difficulty')
user_inp = input('Enter difficulty: ')
vals.append(user_inp)

# Category
keys.append('Category')
user_inp = input('Enter category: ')
vals.append(user_inp)

pose_info = {}
for count, key in enumerate(keys):
    pose_info.update({key : vals[count]})

yoga_dict.update({key1 : pose_info})


with open('%s/Documents/Python/Yoga_Bot/Library/yoga_poses.json'%(user_path), 'w') as fp:
    json.dump(yoga_dict, fp)
