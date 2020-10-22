# Instagram: Find who does NOT follow you

## What is it
On Instagram, you follow some people (following).  Some people follow you (followers).  But, there are some people you follow, and they are not following you back.  This project helps you find those people!

## What it does
This Python script does the following:
* Using [Selenium](https://www.google.com/search?q=selenium&oq=selenium&aqs=chrome..69i57.1488j0j1&sourceid=chrome&ie=UTF-8), the script logs in with your Instagram account username and password.
* Then, it goes to a specific user (it goes to each one of the user's profiles provided in the *users.json* file) and it tracks the names of all the followers and following of this user.
* It compares the 2 different lists, and prints the people you follow, and they are not following you back.
* It repeats the same for the rest of the users in the *users.json* file

# How to use it:

## Requirements:
* Python3, pip3

## Steps:
1. Clone the current directory.
2. Install selenium:
```
pip3 install selenium
```
3. If you are using Chrome as your preferred browser, download ChromeDriver:: [Download Link](https://sites.google.com/a/chromium.org/chromedriver/home)
If you are using another browser download the corresponding web driver for it.
4. Export as environmental variables your Instagram username and password:
```
export insta_username="your_username"
export insta_password="your_password"
```
5. Add the Instagram users you want to be checked (by providing their username) at the *users.json* file.
6. You can now run the script!
```
python3 main.py
```
