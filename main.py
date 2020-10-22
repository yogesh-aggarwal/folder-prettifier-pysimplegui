import json
from time import sleep

import requests
from selenium import webdriver

isLogin = False
base = "https://instagram.com"


options = webdriver.ChromeOptions()
options.add_argument("--window-size=1300,800")
# options.add_argument("headless")
client = webdriver.Edge("msedgedriver")
# Getting credentials from file
with open("credentials.json") as f:
    credentials = json.loads(f.read())
    uname = credentials["uname"]
    pword = credentials["pword"]
    del credentials


def login(uname=uname, pword=pword):
    global isLogin
    if not isLogin:
        client.get(base)
        while True:
            try:
                client.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input'
                ).send_keys(uname)
                client.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input'
                ).send_keys(pword)
                break
            except:
                continue

        client.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div'
        ).click()

        while True:
            try:
                sleep(1)
                client.find_element_by_xpath(
                    "/html/body/div[4]/div/div/div[3]/button[2]"
                ).click()
                break
            except:
                continue
        isLogin = True


def getProfilePicture(uname=uname):
    client.get(f"{base}/{uname}")
    sleep(1)
    imgUrl = client.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/header/div/div/span/img'
    ).get_attribute("src")
    with open(f"{uname}.png", "wb") as f:
        f.write(requests.get(imgUrl).content)


def followUnames(unames, uname=uname):
    login()

    for followUname in unames:
        client.get(f"{base}/{followUname}")
        sleep(1)
        client.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button'
        ).click()


def unfollowUnames(unames, uname=uname):
    login()

    for unfollowUname in unames:
        client.get(f"{base}/{unfollowUname}")
        sleep(1)
        client.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button'
        ).click()
        sleep(0.5)
        client.find_element_by_xpath(
            "/html/body/div[4]/div/div/div[3]/button[1]"
        ).click()


def _getAllFollow(following=True, show=True, uname=uname):
    login()
    client.get(f"{base}/{uname}")
    sleep(1)
    client.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'
        if following
        else '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'
    ).click()
    sleep(1)
    # client.execute_script("arguments[0].scollIntoView()", listBox)
    lastHt, currHt = 0, 1
    while lastHt < currHt:
        lastHt = currHt
        sleep(1)
        listBox = client.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        currHt = client.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight; return arguments[0].scrollHeight;",
            listBox,
        )

    unames = client.find_elements_by_class_name("FPmhX")

    unamesFinal = []
    for uname in unames:
        print(uname.get_attribute("title")) if show else False
        unamesFinal.append(uname.get_attribute("title"))

    return unamesFinal


def getAllFollowing(uname=uname):
    return _getAllFollow(uname, pword, following=True)


def getAllFollowers(uname=uname):
    return _getAllFollow(uname, pword, following=False)


def _getFollowNotFollow(arr, notArr, uname=uname):
    notUnames = []
    for uname in arr:
        notUnames.append(uname) if uname not in notArr else False

    return notUnames


def getFollowersButNotFollowing(show=True, uname=uname):
    final = _getFollowNotFollow(
        _getAllFollow(following=False, show=False),
        _getAllFollow(following=True, show=False),
    )
    print(final) if show else False
    return final


def getFollowingButNotFollowers(show=True, uname=uname):
    final = _getFollowNotFollow(
        _getAllFollow(following=True, show=False),
        _getAllFollow(following=False, show=False),
    )
    print(final) if show else False
    return final


def unfollowNotFollowing(uname=uname):
    unfollowUnames(getFollowingButNotFollowers(show=False))


def followNotFollowers(uname=uname):
    followUnames(getFollowersButNotFollowing(show=False))


def unfollowAll(uname=uname):
    unfollowUnames(_getAllFollow(following=True, show=False),)


def unfollowFollowers(uname=uname):
    unfollowUnames(_getAllFollow(following=False, show=False),)

# getProfilePicture("efficient-coder")
client.quit()


