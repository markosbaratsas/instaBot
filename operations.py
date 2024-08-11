import json
from selenium import webdriver
import sys
import os
from time import sleep


def read_file(file):
    with open(file) as json_file:
        data = json.load(json_file)
    return data

def write_file(file, data):
    with open(file, 'w') as outfile:
        json.dump(data, outfile)

def start_browser():
    data = read_file("information.json")
    if data["driver"] == "Firefox":
        browser = webdriver.Firefox(executable_path=data["path_to_driver"])
    elif data["driver"] == "Chrome":
        browser = webdriver.Chrome(executable_path=data["path_to_driver"])

    browser.get("https://www.instagram.com/?hl=el")
    return browser

def users_to_look():
    return read_file("information.json")["users"]

def check_unfollow_credentials(browser):
    if ("insta_username" not in os.environ) or ("insta_password" not in os.environ):
        print("Browser quitted. Please export insta_username and insta_password!")
        browser.quit()
        sys.exit(1)

    credentials = {"username":os.environ["insta_username"], "password":os.environ["insta_password"]}
    users_names = users_to_look()

    if len(users_names) > 1 or credentials["username"] != users_names[0]:
        print("Something is wrong!")
        print(
        """In order to unfollow those who do not follow you, you must export your credentials using
              export insta_username="your_username"
              export insta_password="your_password"

        AND fill the necessary information on the `information.json` file!""")
        browser.quit()
        sys.exit(1)

def instagram_cookies_accept(browser: webdriver.Firefox):
    # accept coockies
    sleep(2)
    accept = browser.find_element_by_class_name("_a9_0")
    accept.click()
    sleep(2)
