from requests_html import HTMLSession
import re
import constants
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class ZalandoScraping:
    def __init__(self, url):
        self.url = url
        self.text = ""
        self.__fetch_page()
        self.soup = BeautifulSoup(self.text, 'html.parser')

    def __fetch_page(self):
        session = HTMLSession()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
        session.set_header(headers)
        session.visit(self.url)
        self.text = session.body()

    def __get_title(self):
        return self.soup.find("h1", {"class": constants.ZA_C_TITLE}).text

    def __get_brand(self):
        return self.soup.find("h3", {"class": constants.ZA_C_BRAND}).text

    def __get_currency(self):
        tld = urlparse(self.url).netloc.replace("www.zalando.", "").split(":")[0]
        return constants.CURRENCIES[tld.upper()]

    def __get_price(self):
        for elem in self.soup.find_all("span", {"class": constants.ZA_C_PRICE}):
            if elem.text != "":
                value = float(re.findall("([0-9]+(?:.|,)[0-9]+)", elem.text)[0].replace(",", "."))
                currency = self.__get_currency()
                return [value, currency]

    def __get_color(self):
        div = self.soup.find("div", {"class": constants.ZA_C_COLORLST})
        return div.find("span", {"class": constants.ZA_C_COLOR}).text

    def __get_images(self):
        ul = self.soup.find("ul", {"class": constants.ZA_C_IMGLST})
        return [x["src"].split("=")[0] + "=1080" for x in ul.find_all("img", {"class": constants.ZA_C_IMG})]

    def __get_condition(self):
        for p in constants.PREOWNED_KEYWORDS:
            if p in self.__get_title():
                return p
        return "new"

    def __get_reviews(self):
        review_row = self.soup.find_all("div", {"id": constants.ZA_ID_REVIEW})
        if len(review_row):
            count = int(re.findall(r"\(\d+\)", review_row[0].find("h5").text)[0][1:-1])
            if count:
                rating = float(review_row[0].find("span", {"class": constants.ZA_C_RATING}).text)
                return [count, rating]
        return [0, "NaN"]

    def __get_moreinfo(self, position):
        infos = {}
        moreinfo_section = self.soup.find_all("div", {"class": constants.ZA_C_INFOMAIN})[position]
        subsection = moreinfo_section.find("div", {"class": constants.ZA_C_INFOSUB})
        rows = subsection.find_all("span", {"class": constants.ZA_C_INFOROW})
        if len(rows) % 2 != 0:
            infos["Info"] = rows[0].text
            rows.pop(0)
        for i in range(0, len(rows), 2):
            attribute = rows[i].text.replace(":", "")
            value = rows[i + 1].text
            infos[attribute] = value
        return infos

    def __get_material(self):
        return self.__get_moreinfo(0)

    def __get_details(self):
        return self.__get_moreinfo(1)

    def __get_sizeinfo(self):
        return self.__get_moreinfo(2)

    def get_data(self):
        title = self.__get_title()
        brand = self.__get_brand()
        price, currency = self.__get_price()
        color = self.__get_color()
        condition = self.__get_condition()
        review_count, rating = self.__get_reviews()
        images = self.__get_images()
        details = {}
        for d in [self.__get_material(), self.__get_details(), self.__get_sizeinfo()]:
            details.update(d)
        return {"title": title, "brand": brand, "price": price, "currency": currency, "color": color,
                "condition": condition, "review_count": review_count, "rating": rating,
                "details": details, "images": images}


class HMScraping:
    def __init__(self, url):
        self.url = url
        self.text = ""
        self.__fetch_page()
        self.soup = BeautifulSoup(self.text, 'html.parser')

    def __fetch_page(self):
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
        req = session.get(url=self.url, headers=headers)
        if req.status_code != 200:
            return False
        else:
            self.text = req.text

    def __get_title(self):
        return self.soup.find("h1", {"class": constants.HM_C_TITLE}).text

    def __get_currency(self):
        country = self.soup.find("html")["lang"].split("-")[-1]
        return constants.CURRENCIES[country]

    def __get_price(self):
        value = re.findall("[0-9]+(?:.|,)[0-9]+", str(self.soup.find("span", {"class": constants.HM_C_PRICE}).text))
        return value, self.__get_currency()

    def __get_color(self):
        return self.soup.find("h3", {"class": constants.HM_C_COLOR}).text

    def __get_images(self):
        return [x["src"] for x in self.soup.find_all("img", {"class": constants.HM_C_IMG})]

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
        print(self.soup.find("span", {"class": "reviews-number"}))
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
