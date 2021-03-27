# Instagram: Find who does NOT follow you back

## Description
On Instagram, you follow some people (following).  Some people follow you (followers).  But, there are some people you follow, and they are not following you back. This repository was created to automate the process of finding those people. Instead of trusting third-party apps and providing them with your instagram password, this repository can be used to automate the whole procedure, without having to share your passwords with any app!

## How it works
This Python script does the following:
* Using [Selenium](https://www.google.com/search?q=selenium&oq=selenium&aqs=chrome..69i57.1488j0j1&sourceid=chrome&ie=UTF-8), the script will login to your Instagram account, using your username and password.
* Then, it goes to a specific user (it goes to each one of the user's profiles provided in the *information.json* file) and it tracks the names of all the followers and following of this user.
* It compares the 2 different lists, and prints the people you follow, and they are not following you back.
* It repeats the same for the rest of the users in the *information.json* file

## What can be done using this repository
1. Find the people that you follow, but they are not following you back. This can, also, be used to find the corresponding people for some other account, as long as YOUR account has access to view their followers and following.
2. Find the people that you follow, but they are not following you back PLUS unfollow a number of those people.


# How to use it:

## Requirements:
* Python3, pip3

## Instructions:
1. Clone the current directory.
2. Install the requirements:
```
pip3 install -r requirements.txt
```
3. If you are using Firefox, you can download [geckodriver](https://github.com/mozilla/geckodriver/releases). If you are using Chrome as your preferred browser, download [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/home).
4. Export as environmental variables your Instagram username and password:
```
export insta_username="your_username"
export insta_password="your_password"
```
5. Fill in the necessary information required at the `information.json` file. Inside the json file, on the `driver` option, provide one of the following: 
* Firefox
* Chrome
6. Now, you can execute the script. To find those people execute:
```
python3 main.py
```
To find those people and unfollow some of them afterwards (e.g. 100 people), execute the following:
```
python3 main.py unfollow 100
```
```
# or unfollow all of them by running
python3 main.py unfollow
```
