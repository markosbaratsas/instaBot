from selenium import webdriver
import os
from time import localtime, sleep
import sys
from selenium.webdriver.common.keys import Keys

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

def you_follow_them_but_they_not_you(browser, i):
    browser.get("https://www.instagram.com/"+i)
    sleep(2)
    followers = find_followers_or_following(browser, i, "followers")
    print(i, "has", len(followers), "followers.")

    browser.get("https://www.instagram.com/"+i)
    sleep(1)
    following = find_followers_or_following(browser, i, "following")
    print(i, "is following", len(following), "people.")

    ret = you_follow_them_but_they_not_you_check(followers,following)
    print("You follow them but not them you for user: ", i)
    print(ret)
    return ret 

def send_msg(browser, list_unfollowers, person):
    browser.get("https://www.instagram.com/"+person)
    sleep(2)

    browser.find_element_by_class_name("_8A5w5").click()
    sleep(2)

    try:
        browser.find_element_by_class_name("HoLwm").click()
    except:
        print("sth went wrong1")

    sleep(2)

    text_area = browser.find_elements_by_tag_name("textarea")[0]
    print(text_area)    
    
    text_area.send_keys("Greetings from InstUnfollow! I will send you the usernames of those you follow, but they are not following you back.")
    sleep(0.5)
    try:
        browser.find_elements_by_class_name("y3zKF")[3].click()
    except:
        browser.find_elements_by_class_name("y3zKF")[2].click()
    sleep(2)
    
    if len(list_unfollowers) >= 1:
        text_area.send_keys("@")
    for i in range(0, len(list_unfollowers), 50):
        text_area.send_keys(", @".join(list_unfollowers[i:i+50]))
        sleep(1)
        try:
            browser.find_elements_by_class_name("y3zKF")[3].click()
        except:
            browser.find_elements_by_class_name("y3zKF")[2].click()
        sleep(1)

    if len(list_unfollowers) == 0:
        text_area.send_keys("All the people you follow, follow you back! Good job! You are really cool and popular and awesome...")
        sleep(0.5)
        try:
            browser.find_elements_by_class_name("y3zKF")[3].click()
        except:
            browser.find_elements_by_class_name("y3zKF")[2].click()
        sleep(2)


    text_area.send_keys("That's all from me. See you next time!")
    try:
        browser.find_elements_by_class_name("y3zKF")[3].click()
    except:
        browser.find_elements_by_class_name("y3zKF")[2].click()
    sleep(1)
    
def go_follow_that_person(browser, i):
    browser.get("https://www.instagram.com/"+i)

    count_followers = int(browser.execute_script("return document.getElementsByClassName('-nal3')[1].getElementsByClassName('g47SY')[0].textContent").replace(",",""))
    print("Number of followers:", count_followers)
    count_following = int(browser.execute_script("return document.getElementsByClassName('-nal3')[2].getElementsByClassName('g47SY')[0].textContent").replace(",",""))
    print("Number of following:", count_following)

    if count_followers >= 2000 or count_following >= 2000:
        return False
        
    if len(browser.find_elements_by_class_name("y3zKF")) == 0:
        return True
        
    try:
        button = browser.find_elements_by_class_name("y3zKF")
        button[0].click()
    except:
        pass

    count_sec = 600

    while count_sec > 0:
        browser.get("https://www.instagram.com/"+i)
        sleep(30)
        if len(browser.find_elements_by_class_name("y3zKF")) == 0:
            return True        
        count_sec -= 30

    return False


def go_unfollow_that_person(browser, i):
    browser.get("https://www.instagram.com/"+i)
    
    browser.find_elements_by_class_name("_8A5w5")[1].click()

    sleep(1)

    browser.find_elements_by_class_name("Cab_")[0].click()