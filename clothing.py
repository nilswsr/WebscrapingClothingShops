import json
import time
from selenium import webdriver


def get_data_main(obj):
    article_id = obj.get_article_id()
    title = obj.get_title()
    brand = obj.get_brand()
    color = obj.get_color()
    category = obj.get_category()
    target_gender = obj.get_target_gender()
    description = obj.get_description()
    current_price, original_price, discounted = obj.get_price()
    currency = obj.get_currency()
    images = obj.get_images()
    review_count, avrg_rating = obj.get_reviews()
    return {"articleId": article_id,
            "title": title,
            "brand": brand,
            "color": color,
            "category": category,
            "targetGender": target_gender,
            "description": description,
            "price": {
                "currentPrice": current_price,
                "originalPrice": original_price,
                "isDiscounted": discounted
            },
            "currency": currency,
            "images": images,
            "reviews": {
                "reviewCount": review_count,
                "averageRating": avrg_rating
            }
            }


class ZalandoScraping:
    def __init__(self, url):
        self.url = url
        self.product_data = self.__fetch_page()

    def __fetch_page(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        product_data = driver.execute_script("return document.getElementById('z-vegas-pdp-props').textContent")
        driver.close()
        return json.loads(product_data[product_data.index("{"):product_data.rindex("}")+1])["model"]["articleInfo"]

    def get_article_id(self):
        return self.product_data["id"]

    def get_title(self):
        return self.product_data["name"]

    def get_brand(self):
        return self.product_data["brand"]["name"]

    def get_category(self):
        return self.product_data["product_group"]

    def get_target_gender(self):
        return self.product_data["targetGroups"]["gender"][0]

    def get_color(self):
        return self.product_data["color"]

    def get_description(self):
        return None

    def get_price(self):
        current_price = self.product_data["units"][0]["displayPrice"]["price"]["value"]
        original_price = self.product_data["units"][0]["displayPrice"]["originalPrice"]["value"]
        discounted = self.product_data["units"][0]["displayPrice"]["isDiscounted"]
        return current_price, original_price, discounted

    def get_currency(self):
        return self.product_data["units"][0]["displayPrice"]["price"]["currency"]

    def get_images(self):
        image_lst = self.product_data["media"]["images"]
        return [x["sources"]["zoom"] for x in image_lst]

    def get_reviews(self):
        return int(self.product_data["reviewsCount"]), float(self.product_data["averageStarRating"])

    def get_data(self):
        return get_data_main(self)


class HMScraping:
    def __init__(self, url):
        self.url = url
        self.product_data, self.product_details = self.__fetch_page()

    def __fetch_page(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        product_data = driver.execute_script("return document.getElementById('product-schema').textContent")
        product_details = driver.execute_script("return productArticleDetails[hm.product.getArticleId()]")
        driver.close()
        return json.loads(product_data), product_details

    def get_article_id(self):
        return self.product_data["sku"]

    def get_title(self):
        return self.product_data["name"]

    def get_brand(self):
        return self.product_data["brand"]["name"]

    def get_category(self):
        return self.product_data["category"]["name"]

    def get_target_gender(self):
        return None

    def get_color(self):
        return self.product_data["color"]

    def get_description(self):
        return self.product_data["description"]

    def get_price(self):
        current_price = self.product_data["offers"][0]["price"]
        original_price = current_price
        discounted = False
        return current_price, original_price, discounted

    def get_currency(self):
        return self.product_data["offers"][0]["priceCurrency"]

    def get_images(self):
        return [x["image"] for x in self.product_details["images"]]

    def get_reviews(self):
        return None, None

    def get_data(self):
        return get_data_main(self)


class ASOSScraping:
    def __init__(self, url):
        self.url = url
        self.product_data = self.__fetch_page()

    def __fetch_page(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        product_data = json.loads(driver.execute_script("return JSON.stringify(window.asos.pdp)"))
        driver.close()
        return product_data

    def get_article_id(self):
        return self.product_data["config"]["product"]["id"]

    def get_title(self):
        return self.product_data["config"]["product"]["name"]

    def get_brand(self):
        return self.product_data["config"]["product"]["brandName"]

    def get_category(self):
        return self.product_data["config"]["product"]["productType"]["name"]

    def get_target_gender(self):
        return self.product_data["config"]["product"]["gender"]

    def get_color(self):
        return self.product_data["config"]["product"]["variants"][0]["colour"]

    def get_description(self):
        return None

    def get_price(self):
        current_price = float(self.product_data["stockPrice"][0]["productPrice"]["current"]["value"])
        original_price = self.product_data["stockPrice"][0]["productPrice"]["rrp"]["value"]
        if original_price:
            original_price = float(original_price)
        else:
            original_price = current_price
        discounted = self.product_data["stockPrice"][0]["productPrice"]["isOutletPrice"]
        return current_price, original_price, discounted

    def get_currency(self):
        return self.product_data["stockPrice"][0]["productPrice"]["currency"]

    def get_images(self):
        return [x["url"] for x in self.product_data["config"]["product"]["images"]]

    def get_reviews(self):
        return None, None

    def get_data(self):
        return get_data_main(self)
