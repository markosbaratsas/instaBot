from selenium import webdriver
import os
import json
from time import localtime, sleep
import sys

def start_browser():
    browser = webdriver.Chrome(executable_path='/home/markos/Downloads/chromedriver_linux64/chromedriver')
    browser.get("https://www.instagram.com/?hl=el")
    return browser

def login(browser):
    if ("insta_username" not in os.environ) or ("insta_password" not in os.environ):
        print("Please export insta_username and insta_password")
        browser.quit()
        sys.exit(1)

    credentials = {"username":os.environ['insta_username'], "password":os.environ['insta_password']}

    username = browser.find_element_by_name("username")
    username.send_keys(credentials["username"])

    password = browser.find_element_by_name("password")
    password.send_keys(credentials["password"])

    sleep(0.5)
    submit = browser.find_element_by_css_selector("[type='submit']")
    submit.click()

    sleep(5)

    # not_now = browser.find_element_by_class_name("yWX7d")
    # not_now.click()
    #
    # sleep(5)
    # not_now2 = browser.find_element_by_class_name("HoLwm")
    # not_now2.click()

def instagram_cookies_accept(browser):
    # accept coockies
    accept = browser.find_element_by_class_name("bIiDR")
    accept.click()
    sleep(2)

def users_to_look():
    return read_file("files/users.json")

def check_unfollow_credentials(browser):
    if ("insta_username" in os.environ) or ("insta_password" in os.environ):
        print("Browser quitted. Please export insta_username and insta_password!")
        browser.quit()
        sys.exit(1)

    credentials = {"username":os.environ['insta_username'], "password":os.environ['insta_password']}
    users_names = users_to_look()
    print(credentials["username"], users_names[0])

    if len(users_names) > 1 or credentials["username"] != users_names[0]:
        print("Something is wrong!")
        print(
        """In order to unfollow those who do not follow you, you must export your credentials using
              export insta_username="your_username"
              export insta_password="your_password"

        AND give ONLY your username on files/users.json!""")
        browser.quit()
        sys.exit(1)


def read_file(file):
    with open(file) as json_file:
        data = json.load(json_file)
    return data

def write_file(file, data):
    with open(file, 'w') as outfile:
        json.dump(data, outfile)
