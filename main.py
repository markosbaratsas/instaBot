from math import floor
from time import localtime, sleep
import sys
from functools import partial
from random import random, seed

from signal_handler import signal, signal_handler
from actions import start_browser, login, instagram_cookies_accept, users_to_look, check_unfollow_credentials, write_file


def find_followers_or_following(browser, username,ers_or_ing):
    if(ers_or_ing == "followers"):
        count = int(browser.execute_script("return document.getElementsByClassName('-nal3')[1].getElementsByClassName('g47SY')[0].textContent").replace(",",""))
        print("Number of followers:", count)
    else:
        count = int(browser.execute_script("return document.getElementsByClassName('-nal3')[2].getElementsByClassName('g47SY')[0].textContent").replace(",",""))
        print("Number of following:", count)

    button = browser.find_element_by_css_selector("[href='/" + username + "/" + ers_or_ing + "/']")
    button.click()

    if count > 0:
        # scrolling down
        currentLen = 1
        sleep(2)
        printing_help = 0
        while currentLen < count:
            previousLen = currentLen
            browser.execute_script("document.getElementsByClassName('_0imsa')["+str(int(currentLen-1))+"].scrollIntoView();")
            sleep(0.5)
            currentLen = browser.execute_script("return document.getElementsByClassName('_0imsa').length")

            if floor(currentLen/50)>printing_help and previousLen != currentLen:
                printing_help = floor(currentLen/50)
                current_time = localtime()
                print("I have seen", currentLen, "/", count, "sofar. Time:   ",  localtime().tm_hour, ":", localtime().tm_min, ":", localtime().tm_sec)
            if previousLen == currentLen and localtime().tm_min > current_time.tm_min:
                browser.execute_script("document.getElementsByClassName('_0imsa')["+str(max(int(currentLen-12), 0))+"].scrollIntoView();")
                sleep(3)
            if previousLen == currentLen and localtime().tm_min > current_time.tm_min and currentLen >= count-5:
                break

        print("end")
        users = browser.execute_script(
        """
            let users = document.getElementsByClassName("_0imsa")
            let arr = [];
            for (i = 0; i < users.length; i++) {
                arr.push(users[i].title);
            }
            return arr;
        """)

        return users
    else:
        return []

def you_follow_them_but_they_not_you(followers, following):
    set_of_followers = set(followers)

    ret = []
    for i in following:
        if i not in set_of_followers:
            ret.append(i)

    return ret


def main_script(browser):
    instagram_cookies_accept(browser)

    login(browser)

    users_names = users_to_look()

    for i in users_names:
        browser.get("https://www.instagram.com/"+i)
        sleep(2)
        followers = find_followers_or_following(browser, i, "followers")
        print(i, "has", len(followers), "followers.")
        write_file("files/followers.json", followers) # for debuging reasons

        browser.get("https://www.instagram.com/"+i)
        sleep(1)
        following = find_followers_or_following(browser, i, "following")
        print(i, "is following", len(following), "people.")
        write_file("files/following.json", following) # for debuging reasons

        ret = you_follow_them_but_they_not_you(followers,following)
        print("You follow them but not them you for user: ", i)
        print(ret)

        sleep(5)

    return ret #needed for unfollow

def unfollow_script(browser, unfollow_list):
    # Suppose we already are at following tab. And all the people we follow are already loaded on the screen.
    # Then we can run the below script
    unfollowed_sofar = []
    seed(1)

    for i in unfollow_list:
        if i == "maaritinaaa":
            continue

        unfollow_button = browser.execute_script(
        """
            node = document.querySelector('[title=\"""" + i + """\"]');
            return node.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector('[type="button"]');
        """)
        unfollow_button.click()
        sleep(0.5 + random())

        confirm = browser.execute_script(
        """
            return document.getElementsByClassName("-Cab_")[0];
        """)
        confirm.click()

        print("Unfollowed: ", i)
        unfollowed_sofar.append(i)

        sleep(3 + 7*random()) # sleeping so that instagram won't detect us as a Bot

    print("Unfollowed these people:")
    print(unfollowed_sofar)


if __name__ == "__main__":
    browser = start_browser()

    signal.signal(signal.SIGINT,  partial(signal_handler, browser))

    if len(sys.argv) == 1:
        main_script(browser)
    elif len(sys.argv) == 2 and sys.argv[1] == "login":
        instagram_cookies_accept(browser)

        login(browser)
        sleep(1000000)
    elif len(sys.argv) == 2 and sys.argv[1] == "unfollow": # unfollow those who does not follow you back
        check_unfollow_credentials(browser)

        print("First part: Let's find those people!")
        unfollow_list = main_script(browser)

        print("Second part: Let's unfollow those people!")
        unfollow_script(browser, unfollow_list)

    browser.quit()
    print("Browser succefully quitted!")
