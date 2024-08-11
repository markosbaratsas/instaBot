from selenium import webdriver
import os
from time import localtime, sleep
import sys

from actions import find_followers_or_following, you_follow_them_but_they_not_you_check, unfollow_some_of_them_do_it
from operations import read_file, write_file, users_to_look

def login(browser):
    if ("insta_username" not in os.environ) or ("insta_password" not in os.environ):
        print("Please export insta_username and insta_password")
        browser.quit()
        sys.exit(1)

    credentials = {"username":os.environ['insta_username'], "password":os.environ['insta_password']}

    username = browser.find_element_by_name("username")
    username.send_keys(credentials["username"])

    sleep(1)
    password = browser.find_element_by_name("password")
    password.send_keys(credentials["password"])

    sleep(1)
    submit = browser.find_element_by_css_selector("[type='submit']")
    submit.click()

    sleep(5)

    return credentials["username"]

def you_follow_them_but_they_not_you(browser):
    users_names = users_to_look()

    for i in users_names:
        browser.get("https://www.instagram.com/"+i)
        sleep(2)
        followers = find_followers_or_following(browser, i, "followers")
        print(i, "has", len(followers), "followers.")
        write_file("files/"+ i +"_followers.json", followers) # for debuging reasons

        browser.get("https://www.instagram.com/"+i)
        sleep(1)
        following = find_followers_or_following(browser, i, "following")
        print(i, "is following", len(following), "people.")
        write_file("files/"+ i +"_following.json", following) # for debuging reasons

        ret = you_follow_them_but_they_not_you_check(followers,following)
        ret.sort()
        write_file("files/"+ i +"_you_follow_them_but_they_not_you.json", ret) # for debuging reasons
        print("You follow them but not them you for user: ", i)
        print(ret)

        sleep(5)

    return ret #needed for unfollow

def unfollow_script(browser, username, find_followers, count):
    if find_followers:
        browser.get("https://www.instagram.com/"+username)
        sleep(2)
        followers = find_followers_or_following(browser, username, "followers")
        print(username, "has", len(followers), "followers.")
        write_file("files/"+ username +"_followers.json", followers) # for debuging reasons
        followers = set(followers)
    else:
        followers = set(read_file("files/"+ username +"_followers.json"))

    unfollowed = unfollow_some_of_them_do_it(browser, username, int(count), followers)

    print(username, "just unfollowed", len(unfollowed), "people.")

    if os.path.exists("files/"+ username +"_unfollowed.json"):
        unfollowed_so_far = read_file("files/"+ username +"_unfollowed.json")
    else:
        unfollowed_so_far = []
    unfollowed = unfollowed_so_far + unfollowed
    write_file("files/"+ username +"_unfollowed.json", unfollowed) # for debuging reasons
