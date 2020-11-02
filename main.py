from time import sleep
import sys
from functools import partial
import traceback
# from selenium import webdriver

from signal_handler import signal, signal_handler
from operations import start_browser, instagram_cookies_accept, check_unfollow_credentials
from modes import login, you_follow_them_but_they_not_you, unfollow_script


if __name__ == "__main__":
    browser = start_browser()

    signal.signal(signal.SIGINT,  partial(signal_handler, browser))

    sleep(1)
    instagram_cookies_accept(browser)
    username = login(browser)

    try:
        if len(sys.argv) == 1:
            you_follow_them_but_they_not_you(browser)
        elif len(sys.argv) == 2 and sys.argv[1] == "login":
            sleep(1000000)
        elif len(sys.argv) == 3 and sys.argv[1] == "unfollow": # unfollow those who does not follow you back
            check_unfollow_credentials(browser)
            how_many_to_unfollow = sys.argv[2]
            unfollow_script(browser, username, True, how_many_to_unfollow)
        elif len(sys.argv) == 4 and sys.argv[1] == "unfollow" and sys.argv[3] == "skip_finding_followers": # unfollow those who does not follow you back
            check_unfollow_credentials(browser)
            how_many_to_unfollow = int(sys.argv[2])
            unfollow_script(browser, username, False, how_many_to_unfollow)
    except:
        browser.quit()
        print("Something went wrong...")
        traceback.print_exc()
        sys.exit(1)

    browser.quit()
    print("Browser succefully quitted!")
