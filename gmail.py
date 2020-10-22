from selenium import webdriver
import os
import time
import requests
import pyautogui
import imquality.brisque as brisque
import PIL
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1300,800")
options.add_argument("--headless=true")
# client = webdriver.Edge("msedgedriver")
client = webdriver.Chrome("chromedriver", chrome_options=options)
# Getting credentials from file

# hotelNames = input("Hotel name: ").split(", ")
hotelNames = [
    # "Radisson Blu Plaza",
    # "The Leela Palace new delhi",
    "The Imperial"
]

try:
    os.mkdir("hotels")
except:
    pass

os.chdir("hotels")

pyautogui.hotkey("win", "up")


def visitAgoda(hotel):
    client.get("https://google.com")
    client.find_element_by_xpath(
        '//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input'
    ).send_keys(f"{hotel} agoda")
    client.find_element_by_xpath(
        '//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input'
    ).send_keys(Keys.ENTER)
    websiteUrl = client.find_element_by_xpath(
        "/html/body/div[6]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div[1]/a"
    ).get_attribute("href")
    time.sleep(1)
    client.get(websiteUrl)


def createDir(name):
    os.makedirs(name, exist_ok=True)


def downloadImage(url, hotel, count, category, score=True):
    createDir(f"{category}")
    os.chdir(category)

    with open(f"{hotel} - {count}.png", "wb") as f:
        f.write(requests.get(url).content)

    img = PIL.Image.open(f"{hotel} - {count}.png")
    if brisque.score(img) > 40:
        os.remove(f"{hotel} - {count}.png")
    os.chdir("../")


class HandleAgoda:
    def __init__(self):
        self.categories = {
            "rooms": {
                "xpath": "/html/body/div[26]/div/div/div[1]/div[5]/div[2]",
                "imgCount": 7,
            },
            "property": {
                "xpath": "/html/body/div[26]/div/div/div[1]/div[5]/div[3]",
                "imgCount": 7,
            },
            "facilities": {
                "xpath": "/html/body/div[26]/div/div/div[1]/div[5]/div[4]",
                "imgCount": 7,
            },
            "dining": {
                "xpath": "/html/body/div[26]/div/div/div[1]/div[5]/div[5]",
                "imgCount": 7,
            },
            "nerby-attarctions": {
                "xpath": "/html/body/div[26]/div/div/div[1]/div[5]/div[6]",
                "imgCount": 4,
            },
            "other": {
                "xpath": "/html/body/div[26]/div/div/div[1]/div[5]/div[7]",
                "imgCount": 2,
            },
        }
        super().__init__()
        self.closeModals()
        self.openImageSection()
        self.captureImages()

    @staticmethod
    def openImageSection():
        try:
            client.find_element_by_xpath(
                '//*[@id="property-critical-root"]/div/div[3]/div[2]/div[2]/div[1]/div[1]'
            ).click()
        except:
            client.find_element_by_xpath(
                '//*[@id="property-critical-root"]/div/div[4]/div[2]/div[2]/div[1]/div[1]'
            ).click()
        time.sleep(1)

    @staticmethod
    def closeModals():
        client.find_element_by_xpath(
            '//*[@id="SearchBoxContainer"]/div/div/div[2]'
        ).click()
        time.sleep(2)

    def captureImages(self):
        for category in self.categories:
            client.find_element_by_xpath(self.categories[category]["xpath"]).click()

            for i in range(1, self.categories[category]["imgCount"]):
                client.find_element_by_xpath(
                    f"/html/body/div[26]/div/div/div[1]/div[6]/div/div/div/div[{i}]/img"
                ).click()
                time.sleep(0.2)
                imgUrl = client.find_element_by_xpath(
                    f"/html/body/div[26]/div/div/div[1]/div[1]/div/div[{i}]/div/img"
                ).get_attribute("src")
                downloadImage(url=imgUrl, hotel=hotel, count=i, category=category)


for hotel in hotelNames:
    createDir(hotel)
    os.chdir(hotel)
    visitAgoda(hotel)
    HandleAgoda()
    os.chdir("../")
