import json
from selenium import webdriver


class HMScraping:
    def __init__(self, url):
        self.url = url
        self.product_data, self.product_details = self.__fetch_page()

    def __fetch_page(self):
        driver = webdriver.Firefox()
        driver.get(self.url)
        product_data = driver.execute_script("return document.getElementById('product-schema').textContent")
        product_details = driver.execute_script("return productArticleDetails[hm.product.getArticleId()]")
        driver.close()
        return json.loads(product_data), product_details

    def __get_article_id(self):
        return self.product_data["sku"]

    def __get_title(self):
        return self.product_data["name"]

    def __get_brand(self):
        return self.product_data["brand"]["name"]

    def __get_category(self):
        return self.product_data["category"]["name"]

    def __get_target_gender(self):
        return None

    def __get_color(self):
        return self.product_data["color"]

    def __get_description(self):
        return self.product_data["description"]

    def __get_price(self):
        current_price = self.product_data["offers"][0]["price"]
        original_price = current_price
        discounted = False
        return current_price, original_price, discounted

    def __get_currency(self):
        return self.product_data["offers"][0]["priceCurrency"]

    def __get_images(self):
        return [x["image"] for x in self.product_details["images"]]

    def __get_reviews(self):
        return None, None

    def get_data(self):
        article_id = self.__get_article_id()
        title = self.__get_title()
        brand = self.__get_brand()
        color = self.__get_color()
        category = self.__get_category()
        target_gender = self.__get_target_gender()
        description = self.__get_description()
        current_price, original_price, discounted = self.__get_price()
        currency = self.__get_currency()
        images = self.__get_images()
        review_count, avrg_rating = self.__get_reviews()
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
