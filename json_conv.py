'''
Purpose of this file: take a post and convert it to json format we want (refer to READMe.md)
Input: piazza post, filepath
Output: json file produced and added to, or existing json file is modified and added to
'''

import json
import os

from parse_html import parse_def

def get_role_rep(dic):
    role = "instructor"
    if dic['anon'] == 'stud':
        role = "student"
    elif dic['tag_good_arr']:
        role = "student"
    elif dic['type'] == "followup":
        role = "student"
    return role

def get_role_answer(type):
    return 'instructor' if type.startswith("i_") else 'student'

def extract_follow_ups(follow_ups, parent_idx):
    follow_up_list = []
    for follow_up_idx, follow_up in enumerate(follow_ups):
        follow_up_data = {
            "msg_number": f"{parent_idx}.{follow_up_idx + 1}",
            "role": get_role_rep(follow_up),
            "description": parse_def(follow_up['subject']),
            "follow_up": extract_follow_ups(follow_up['children'], f"{parent_idx}.{follow_up_idx + 1}")
        }
        follow_up_list.append(follow_up_data)

    return follow_up_list

def extract_child_history(children, anon_map):
    history = []
    for idx, child in enumerate(children):
        if idx == 0:
            # if the post is marked resolved by an instructor, we start with the thread!!
            if not 'history' in child:
                child_data = {
                "msg_number": str(idx + 1),
                "role": "student",
                "description": parse_def(child['subject']),
                "follow_up": extract_follow_ups(child['children'], idx + 1)
                }
                history.append(child_data)
            # for the first provided "answer" of the thread
            else:
                child_history = child['history'][0]
                child_data = {
                    "msg_number": str(idx + 1),
                    "role": get_role_answer(child['type']),
                    "description": parse_def(child_history['content']),
                    "follow_up": extract_follow_ups(child['children'], idx + 1)
                }
                history.append(child_data)
        # for any follow up discussion!
        else:
            # ensure that we aren't making a whole child for an instructor marking resolved!! child['history'][0]['content'] == 'Resolved.'
            if not 'history' in child:
                child_data = {
                    "msg_number": str(idx + 1),
                    "role": get_role_rep(child),
                    "description": parse_def(child['subject']),
                    "follow_up": extract_follow_ups(child['children'], idx + 1)
                }
                history.append(child_data)
    return history


def extract_post_data(post_data):
    post_number = post_data['nr']
    post_title = post_data['history'][0].get('subject')
    post_description = parse_def(post_data['history'][0].get('content'))
    
    history = extract_child_history(post_data.get('children', []), post_data.get('anon_map', {}))
    
    post_structure = {
        "post_number": post_number,
        "post_title": post_title,
        "description": post_description,
        "history": history
    }
    
    return post_structure

def append_to_json_file(file_path, new_data):
    # if file exists read it 
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    # add new data
    if isinstance(data, list):
        data.append(new_data)
    else:
        data = [new_data]

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def parse(post, file_path):
    post_structure = extract_post_data(post)
    append_to_json_file(file_path, post_structure)