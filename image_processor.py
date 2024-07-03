'''
This file processes images from a given "subject" or "content" depending on 
whether it is the main post, thread, reply etc. 

The respective function in image_processor is called from json_conv.py to append
the image path to the json object for the post and replies.

This file is responsible for handling a message's content. If the message contains
the html key for an image, it will construct the proper link by manipulating the provided
image data in the message (as seen below). Then, it will use this link to download the 
image to an output folder, and then will put the image path in the json object. If 
there is no image for the post, then it will just have an empty string for the image_path
field in the json object. 
'''

import requests
import os
import html

# universal base_url
base_url = "https://cdn-uploads.piazza.com/paste"
output_folder = "output_images"

# Takes ONE content / description from ONE message
# Extracts ALL images from that message and returns them as a list 
def extract_links(content):
    content = html.unescape(content)  # Decode HTML entities
    image_paths = []
    start = 0

    while '<img src="' in content[start:]:
        start_img_tag = content.find('<img src="', start)
        if start_img_tag == -1:
            break
        start_img_tag += len('<img src="')
        
        end_img_tag = content.find('"', start_img_tag)
        if end_img_tag == -1:
            break
        
        img_url = content[start_img_tag:end_img_tag]

        start_prefix = img_url.find('prefix=attach')
        if start_prefix == -1:
            start_prefix = img_url.find('prefix=paste')
            if start_prefix == -1:
                start = end_img_tag
                continue  # Skip this image and continue with the next one
        start_prefix += len('prefix=')
        
        # Find the end of the image path (accounting for multiple extensions and cases)
        extensions = ['.png', '.jpeg', '.jpg', '.PNG', '.JPEG', '.JPG']
        end_positions = {ext: img_url.find(ext, start_prefix) for ext in extensions}
        end_positions = {ext: pos for ext, pos in end_positions.items() if pos != -1}
        
        if not end_positions:
            start = end_img_tag
            continue  # Skip this image and continue with the next one
        
        # Find the earliest end position
        end_ext = min(end_positions, key=end_positions.get)
        end = end_positions[end_ext] + len(end_ext)

        # Extract the image path
        image_path = img_url[start_prefix:end].replace('%2F', '/')
        
        # Append the full URL
        image_paths.append("https://cdn-uploads.piazza.com/" + image_path)
        
        # Update the start index to avoid reprocessing the same section
        start = end_img_tag

    return image_paths

def get_save_path(post_number, msg_number, idx):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return os.path.join(output_folder, f"post_{post_number}_msg_{msg_number}_{idx}.png")


def download_image(image_url, save_path):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
        # print(f"Image successfully downloaded and saved as {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# downloads the image given the link and returns the path
def get_paths(content, msg_number, post_number):
    image_links = extract_links(content)
    image_paths = []
    for idx, link in enumerate(image_links):
        save_path = get_save_path(post_number, msg_number, idx)
        download_image(link, save_path)
        image_paths.append(save_path)
    return image_paths

