import json_conv as converter
import json
import os
import time
import argparse

from piazza_api import Piazza
from piazza_api.exceptions import RequestError
from json_len import calc_len
from dotenv import load_dotenv

load_dotenv('cred.env')

def get_last_post_number(network):
    feed = network.get_feed(limit=9999)
    post_ids = [post['nr'] for post in feed['feed']]
    if post_ids:
        last_post_number = max(post_ids)
    else:
        last_post_number = None
    return last_post_number

def check_stepik(post):
    keywords = ["stepik", "stepnik", "steptik", "skeptik"]
    post_title = post['history'][0].get('subject').lower()
    post_description = post['history'][0].get('content').lower()
    contains = any(keyword in post_title or keyword in post_description for keyword in keywords)
    return contains

def processor(cse_8a, min, max, file_path, filter_func=None):
    for post_number in range(min, max+1):  
        try:
            post = cse_8a.get_post(post_number)  
            if post and 'history' in post and post['history'] and post['type']=="question":
                if check_stepik(post):
                    converter.parse(post, file_path)
        except RequestError as e:
            pass
        time.sleep(2) # kept getting "moving too fast error"

def main():
    parser = argparse.ArgumentParser(description='Process Piazza posts.')
    parser.add_argument('--filter', type=str, default="stepik", help='Filter posts by a keyword (e.g., stepik)')
    parser.add_argument('--min_post', type=int, default=1, help='Minimum post number to process')
    parser.add_argument('--max_post', type=int, default=9999, help='Maximum post number to process')
    parser.add_argument('--file_path', type=str, default='output.json', help='Path to the output file')
    args = parser.parse_args()

    username = os.getenv('PIAZZA_USERNAME')
    password = os.getenv('PIAZZA_PASSWORD')

    if not username or not password:
        raise ValueError("Username or password not set in environment variables.")

    p = Piazza()
    p.user_login(email=username, password=password)
    network = p.network("lueekqs5pbe49z")
    last_post = get_last_post_number(network)

    filter_func = None
    maximum = None
    if args.filter == 'stepik':
        filter_func = check_stepik
    if args.max_post == '9999':
        maximum = last_post = get_last_post_number(network)

    processor(network, args.min_post, args.max_post, args.file_path, filter_func)

if __name__ == "__main__":
    main()

