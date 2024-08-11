from math import floor
from selenium import webdriver
from time import localtime, sleep
from random import random, seed


def find_followers_or_following(browser, username,ers_or_ing):
    if(ers_or_ing == "followers"):
        count = int(browser.execute_script("return document.getElementsByClassName('_a6hd')[1].childNodes[0].title").replace(",","").replace(".",""))
        print("Number of followers:", count)
    else:
        count = int(browser.execute_script("return document.getElementsByClassName('_a6hd')[2].childNodes[1].childNodes[0].innerHTML").replace(",","").replace(".",""))
        print("Number of following:", count)

    button = browser.find_element_by_xpath('//a[@href="'+'/' + username + '/' + ers_or_ing + '/'+'"]')
    button.click()

    if count > 0:
        # scrolling down
        currentLen = 1
        sleep(2)
        printing_help = 0
        current_time = localtime()
        finding_element_with_list = 'document.getElementsByClassName("xyi19xy")[0].childNodes[0].childNodes[0].childNodes'
        while currentLen < count:
            previousLen = currentLen
            browser.execute_script(f"{finding_element_with_list}[{str(int(currentLen-1))}].scrollIntoView();")
            sleep(0.5)
            currentLen = browser.execute_script(f"return {finding_element_with_list}.length")

            if floor(currentLen/50)>printing_help and previousLen != currentLen:
                printing_help = floor(currentLen/50)
                current_time = localtime()
                print("I have seen", currentLen, "/", count, "sofar.\tTime:",  localtime().tm_hour, ":", localtime().tm_min, ":", localtime().tm_sec)
            if previousLen == currentLen and localtime().tm_min > current_time.tm_min:
                browser.execute_script(f"{finding_element_with_list}[{str(max(int(currentLen-12), 0))}].scrollIntoView();")
                print(currentLen)
                sleep(3)
            if previousLen == currentLen and localtime().tm_min > current_time.tm_min and currentLen >= count-5:
                break

        print("end")
        users = browser.execute_script(
        f"""
            let users = {finding_element_with_list}
            let arr = [];
            for (i = 0; i < users.length; i++) {{
                arr.push(users[i].childNodes[0].childNodes[0].childNodes[0].childNodes[1].childNodes[0].childNodes[0].childNodes[0].childNodes[0].innerText);
            }}
            return arr;
        """)
        return users
    else:
        return []

def you_follow_them_but_they_not_you_check(followers, following):
    set_of_followers = set(followers)
    ret = []
    for i in following:
        if i not in set_of_followers:
            ret.append(i)
    return ret

def unfollow_some_of_them_do_it(browser, username, count, followers):
    browser.get("https://www.instagram.com/"+username)
    sleep(2)

    count_following = int(browser.execute_script("return document.getElementsByClassName('-nal3')[2].getElementsByClassName('g47SY')[0].textContent").replace(",",""))
    sleep(1)

    button = browser.find_element_by_css_selector("[href='/" + username + "/following/']")
    button.click()
    sleep(1)

    printing_help = 0
    unfollowed_sofar = []

    total_unfollow = count

    for i in range(0,count_following):
        if count <= 0:
            break

        browser.execute_script("document.getElementsByClassName('_0imsa')[" + str(i) + "].scrollIntoView();")
        sleep(0.5)

        name = browser.execute_script("return document.getElementsByClassName('_0imsa')[" + str(i) + "].title;");

        if name not in followers:
            if len(unfollowed_sofar)%4 == 0 and len(unfollowed_sofar) != 0:
                sleep(20+ 5*random())

            unfollow_button = browser.execute_script(
            """
                node = document.querySelector('[title=\"""" + name + """\"]');
                return node.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector('[type="button"]');
            """)
            unfollow_button.click()

            sleep(1.5 + random())

            confirm = browser.execute_script(
            """
                return document.getElementsByClassName("-Cab_")[0];
            """)
            confirm.click()

            print("Unfollowed: ", name)
            unfollowed_sofar.append(name)

            count = count - 1

            sleep(25 + 5*random()) # sleeping so that instagram won't detect us as a Bot


        if floor(i/50)>printing_help:
            printing_help = floor(i/50)
            current_time = localtime()
            print("I have seen", i, "/", count_following, "and unfollowed", len(unfollowed_sofar), "/", total_unfollow, "sofar. Time:   ",  localtime().tm_hour, ":", localtime().tm_min, ":", localtime().tm_sec)


    print("end")
    return unfollowed_sofar
