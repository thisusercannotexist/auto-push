#!/usr/bin/env python
# coding:utf-8
#   |                                                          |
# --+----------------------------------------------------------+--
#   |   Code by : the king                                     |
#   |   Email   : hack the world                               |
#   |   find him on the dark web                               |
# --+----------------------------------------------------------+--  
# --+----------------------------------------------------------+--
#   |                                                          |

#START{
# IMPORT
import requests
import os
import time
from base64 import b64encode
from hexor import *

# READ ENV VARIABLES
from dotenv import load_dotenv


load_dotenv()
# Read configuration from environment variables
username = os.getenv('GITHUB_USERNAME') or os.getenv('USERNAME')
token    = os.getenv('GITHUB_TOKEN') or os.getenv('TOKEN')

print(f'username: {username}')
print(f'token: {token}')

if not username or not token:
    print("Error: Missing GITHUB_USERNAME or MY_FOLLOWERS in environment.")
    exit(1)

p1 = hexor(False, "hex")

# RESPONE AUTH
HEADERS = {"Authorization": "Basic " + b64encode(f"{username}:{token}".encode('utf-8')).decode('utf-8')}
res = requests.get("https://api.github.com/user", headers=HEADERS)
if res.status_code != 200:
    p1.c("Failure to Authenticate! Please check PersonalAccessToken and Username!", "#ff0000")
    exit(1)
else:
    p1.c("Authentication Succeeded!", "#22a701")

# SESSION HEADER
sesh = requests.session()
sesh.headers.update(HEADERS)

# OUTPUT list of users I'm following
def following():
    target = username
    res = sesh.get(f"https://api.github.com/users/{target}/following")
    linkArray = requests.utils.parse_header_links(res.headers['Link'].rstrip('>').replace('>,<', ',<'))
    url = linkArray[1]['url']
    lastPage = url.split('=')[-1]
    following = []
    print(f'Grabbing {target} Following\nThis may take a while... there are {lastPage} pages to go through.')
    for i in range(1, int(lastPage) + 1):
        res = sesh.get(f"https://api.github.com/users/{target}/following?page={i}").json()
        for user in res:
            following.append(user['login'])
    print(f"Total Following: {len(following)}")
    return following

# OUTPUT list of random users:
def get_random_users(following_list):
    try:
        with open("last_page.txt", "r") as f:
            last_page = int(f.read())
    except:
        last_page = 1
    pages = 30
    print(f'This may take a while... there are {pages} pages to go through.')
    
    new_users = []
    try:
        with open("new_users_list.txt") as file_in:
            new_users = [line.strip() for line in file_in]
    except:
        pass

    fn = open("new_users_list.txt", "a")
    n_users = 0
    for i in range(last_page, last_page + pages):
        res = sesh.get(f"https://api.github.com/users?since={i}").json()
        for user in res:
            if user['login'] not in following_list and user['login'] not in new_users:
                new_users.append(user['login'])
                print(f"Finding {user['login']}")
                fn.write(user['login'] + "\n")
                n_users += 1
    with open("last_page.txt", "w") as f:
        f.write(str(last_page + pages))
    fn.close()
    print(f"Finding {n_users} user(s)")
    return new_users

def following_new(followers_list):
    print("Starting to Follow Users...")
    for user in followers_list:
        time.sleep(2)
        res = sesh.put(f"https://api.github.com/user/following/{user}")
        if res.status_code != 204:
            print("Rate-limited, please wait until it finish!")
            time.sleep(60)
        else:
            print(f"Start Following: {user}")

# RUN
following_list = following()
new_users_list = get_random_users(following_list)
# following_new(new_users_list)
