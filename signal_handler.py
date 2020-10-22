import sys
import signal


def signal_handler(browser, signal, frame):
    browser.quit()
    print('You pressed Ctrl+C! Browser quitted safely.')
    sys.exit(0)
