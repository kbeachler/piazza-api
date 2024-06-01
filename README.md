# General: piazza-api

[![PyPI version](https://badge.fury.io/py/piazza-api.png)](http://badge.fury.io/py/piazza-api)

Unofficial Client for Piazza's Internal API


## Basic Usage

```python
>>> from piazza_api import Piazza
>>> p = Piazza()
>>> p.user_login()
Email: ...
Password: ...

>>> user_profile = p.get_user_profile()

>>> eece210 = p.network("hl5qm84dl4t3x2")

>>> eece210.get_post(100)
...

>>> posts = eece210.iter_all_posts(limit=10)
>>> for post in posts:
...     do_awesome_thing(post)

>>> users = eece210.get_users(["userid1", "userid2"])
>>> all_users = eece210.get_all_users()
```

Above are some examples to get started; more in the documentation (which is coming soon; 
but the code is all Sphinx-style documented and is fairly readable).

You can also use the "internal" PiazzaRPC class which maps more directly
to Piazza's API itself but is not as nice and as intuitive to use as the
`Piazza` class abstraction.

```python
>>> from piazza_api.rpc import PiazzaRPC
>>> p = PiazzaRPC("hl5qm84dl4t3x2")
>>> p.user_login()
Email: ...
Password: ...
>>> p.content_get(181)
...
>>> p.add_students(["student@example.com", "anotherStudent@example.com"])
...
```


## Installation

You've seen this before and you'll see it again.

```bash
# The easy way
pip install piazza-api
```

```bash
# The developer way
git clone https://github.com/hfaran/piazza-api
cd piazza-api
python setup.py develop
```

```bash
# The Docker way
git clone https://github.com/hfaran/piazza-api
cd piazza-api
docker build -t piazza-api .
docker run -it piazza-api:latest
```
# CSE 8A 


## Introduction

Our goal is to extract Stepik-related posts from CSE 8A Spring Piazza (with professor Miranda at UCSD) and put them into a simplified format that can easily be comprehended and used as data for our research. We do this by producing a JSON file with a specific format (shown in the next section) which can be used to easily read a post and the chain of responses associated with it. 

## Dependencies 
Ensure you have the following installed:
```pip install piazza-api python-dotenv beautifulsoup4 lxml```

## Create .env File:
Create a file named cred.env in the same directory as post_processor.py and add your Piazza credentials:

PIAZZA_USERNAME=your_username
PIAZZA_PASSWORD=your_password

## JSON Format

For each post, we have an object represent the main message. This object includes 4 fields: the post number on Piazza (int), the post title (string), post description (string), and the history (list of objects). The post description is basically the body/question posed by the student. The history of a post is where we can track instructor or student responses, or any follow-up discussion on a post. Each object in our history list has four fields as well: message number (int), role (string), description (string), and follow-up (list of objects). The role represents whether the message is by an instructoreo or student, and the follow-up is a list of objects with the exact same format. This is representative of the threads that exist in a Piazza post. It is important to note that either a student or instructor can provide the "answer" to a question, and the student answer will be endorsed. Follow-up discussion can take place between anyone. 

## Usage
The main script that you will interact with is post_processor.py.

``` python3 post_processor.py ```

 In its current state, running the above line will assume default arguments, processing all posts within the Piazza feed, extracting only those pertaining to Stepik, converting them to the proper json format (as seen in json_conv.py) and then dumping these json objects continuously to a file called "output.json". 

 You can add additional arguments to process a specific portion of Piazza posts with a min_post or max_post (each referring to a specific number for the min or max you want to use). You can also specify a filepath that you want to dump the json contents to. 

 Script Arguments
- filter: Filter posts by a keyword (default: "stepik").
- min_post: Minimum post number to process (default: 1).
- max_post: Maximum post number to process (default: 9999). If set to 9999, it will process up to the latest post (as calculated within post_processor.py).
- file_path: Path to the output file (default: 'output.json').

Another example:

```python3 post_processor.py --filter stepik --min_post 1 --max_post 200 --file_path post_data.json```

** note: the only current filter is stepik, we may potentiall add others like lab or PA

## Contribute

* [Issue Tracker](https://github.com/hfaran/piazza-api/issues)
* [Source Code](https://github.com/hfaran/piazza-api)


## License

This project is licensed under the MIT License.


## Disclaimer

This is not an official API. I am not affiliated with Piazza Technologies Inc. 
in any way, and am not responsible for any damage that could be done with it. 
Use it at your own risk.
