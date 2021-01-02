from time import sleep
import sys
from functools import partial
import traceback
# from selenium import webdriver

from signal_handler import signal, signal_handler
from operations import start_browser, instagram_cookies_accept, check_unfollow_credentials
from modes import login, you_follow_them_but_they_not_you, send_msg,  go_follow_that_person, go_unfollow_that_person


if __name__ == "__main__":
    browser = start_browser()

    signal.signal(signal.SIGINT,  partial(signal_handler, browser))

    sleep(1)
    instagram_cookies_accept(browser)
    username = login(browser)
    try:
        all_good = go_follow_that_person(browser, sys.argv[1])
    except:
        all_good = False
        browser.quit()
        print("Something went wrong1...")
        traceback.print_exc()
        sys.exit(1)

    if all_good:
        try:
            unfollowers = you_follow_them_but_they_not_you(browser, sys.argv[1])

            try:
                send_msg(browser, unfollowers, sys.argv[1])

                if len(sys.argv) == 3 and  sys.argv[2] == "unfollow_after":
                    go_unfollow_that_person(browser, sys.argv[1])
                else:
                    print("Not unfollowing", sys.argv[1])

            except:
                browser.quit()
                print("Something went wrong3...")
                traceback.print_exc()
                sys.exit(1)

        except:
            browser.quit()
            print("Something went wrong2...")
            traceback.print_exc()
            sys.exit(1)
    else:
        print("not ok")

    browser.quit()
    print("Browser succefully quitted!")
