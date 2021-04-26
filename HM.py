import constants
import json
from selenium import webdriver
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
        print(driver.execute_script("return [reviewsLabel]"))
        #print(json.dumps(test, indent=2, ensure_ascii=False))
        driver.close()
        return html, product_details

    def __get_title(self):
        return self.soup.find("h1", {"class": constants.HM_C_TITLE}).text.lstrip()

    def __get_currency(self):
        country = self.soup.find("html")["lang"].split("-")[-1]
        return constants.CURRENCIES[country]

    def __get_price(self):
        value = float(self.product_details["whitePriceValue"])
        return value, self.__get_currency()

    def __get_color(self):
        return self.product_details["name"]

    def __get_images(self):
        return [x["image"] for x in self.product_details["images"]]

    def __get_reviews(self):
        """
        print(self.soup.find("h2", {"id": constants.HM_ID_REVIEW}).text)
        review_count = re.findall(r"\(\d+\)", str(self.soup.find("h2", {"id": constants.HM_ID_REVIEW}).text))[0][1:-1]
        if not review_count:
            return [0, "NaN"]
        rating = self.soup.find("div", {"class": constants.HM_C_RATING})
        return review_count, rating
        """
        print(self.soup.find("div", {"class": "sticky-footer"}))
        print(self.soup.find_all("h2", {"id": "js-review-heading"}))
        review_span = self.soup.find_all("h2", {"id": "js-review-heading"})
        review_count = re.findall(r"\(\d+\)", str(self.soup.find("span", {"class": "reviews-number"}).text))[0][1:-1]
        if not review_count:
            return [0, "NaN"]
        rating = self.soup.find("div", {"class": constants.HM_C_RATING})
        return review_count, rating

    def get_data(self):
        title = self.__get_title()
        brand = "H&M"
        price, currency = self.__get_price()
        color = self.__get_color()
        condition = "new"
        review_count, rating = self.__get_reviews()
        images = self.__get_images()
        return {"title": title, "brand": brand, "price": price, "currency": currency, "color": color,
                "condition": condition, "review_count": review_count, "rating": rating, "images": images}
