import json_conv as converter
import json
import os
import time

from piazza_api import Piazza
from piazza_api.exceptions import RequestError
from json_len import calc_len


def check_stepik(post):
    keywords = ["stepik", "stepnik", "steptik", "skeptik"]
    post_title = post['history'][0].get('subject').lower()
    post_description = post['history'][0].get('content').lower()
    contains = any(keyword in post_title or keyword in post_description for keyword in keywords)
    return contains

def processor(min, max, file_path):
    for post_number in range(min, max):  
        try:
            post = cse_8a.get_post(post_number)  
            if post and 'history' in post and post['history'] and post['type']=="question":
                if check_stepik(post):
                    converter.parse(post, file_path)
        except RequestError as e:
            pass
        time.sleep(2) # kept getting "moving too fast error"

p = Piazza()
p.user_login()
cse_8a = p.network("lueekqs5pbe49z")
# inclusive lower bound, exclusive upper bound
processor(1, 200, "post_data.json")
len = calc_len("post_data.json")
print(f"Size of json: {len} ")






### Testing Stuff
'''
post = cse_8a.get_post(89)  
converter.parse(post, "post_data.json") # HARD CODED FILE NAME
post2 = cse_8a.get_post(127)  
converter.parse(post2, "post_data.json") # HARD CODED FILE NAME
'''
