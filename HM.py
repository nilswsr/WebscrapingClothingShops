import constants
import re
import time
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup


class HMScraping:
    def __init__(self, url):
        self.url = url
        self.text, self.product_details = self.__fetch_page()
        self.soup = BeautifulSoup(self.text, "html.parser")

    def __fetch_page(self):
        driver = webdriver.Firefox()
        driver.get(self.url)
        html = driver.execute_script("return document.documentElement.outerHTML")
        product_details = driver.execute_script("return productArticleDetails[hm.product.getArticleId()]")
        #print(json.dumps(ja, indent=2, ensure_ascii=False))
        driver.close()
        return html, product_details

    def __get_title(self):
        return self.soup.find("h1", {"class": constants.HM_C_TITLE}).text.lstrip()

    def __get_currency(self):
        country = self.soup.find("html")["lang"].split("-")[-1]
        return constants.CURRENCIES[country]

    def __get_price(self):
        return float(self.product_details["whitePriceValue"])

    def __get_color(self):
        return self.product_details["name"]

    def __get_images(self):
        return [x["image"] for x in self.product_details["images"]]

    def __get_description(self):
        return self.soup.find("p", {"class": "pdp-description-text"}).text

    def get_data(self):
        title = self.__get_title()
        price, currency = self.__get_price(), self.__get_currency()
        color = self.__get_color()
        description = self.__get_description()
        images = self.__get_images()
        return {"title": title, "brand": "H&M", "price": price, "currency": currency, "color": color,
                "description": description, "condition": "new", "reviews": {"review_count": "-", "rating": "-"},
                "images": images}
