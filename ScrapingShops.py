import json
from selenium import webdriver


def get_data_main(obj):
    """Calls all functions for current scraping object to get all possible data

    :param obj: the Scraping Object for wanted shop
    :return: scraped data
    :rtype: dict
    """
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


class Zalando:
    """Class to scrape Zalando data"""
    def __init__(self, url):
        """sets url and calls __fetch_page()

        :param url: url of product to scrape data from
        """
        self.url = url
        self.product_data = self.__fetch_page()

    def __fetch_page(self):
        """gets product data via webdriver access

        :return: product data
        :rtype: dict
        """
        driver = webdriver.Chrome()
        driver.get(self.url)
        product_data = driver.execute_script("return document.getElementById('z-vegas-pdp-props').textContent")
        driver.close()
        return json.loads(product_data[product_data.index("{"):product_data.rindex("}")+1])["model"]["articleInfo"]

    def get_article_id(self):
        """gather article id

        :return: article id
        :rtype: str
        """
        return self.product_data["id"]

    def get_title(self):
        """gather title

        :return: title
        :rtype: str
        """
        return self.product_data["name"]

    def get_brand(self):
        """gather brand name

        :return: brand name
        :rtype: str
        """
        return self.product_data["brand"]["name"]

    def get_category(self):
        """gather category

        :return: category
        :rtype: str
        """
        return self.product_data["product_group"]

    def get_target_gender(self):
        """gather target gender

        :return: gender
        :rtype: str
        """
        return self.product_data["targetGroups"]["gender"][0]

    def get_color(self):
        """gather color

        :return: color
        :rtype: str
        """
        return self.product_data["color"]

    def get_description(self):
        """gather description

        :return: description
        :rtype: str
        """
        return None

    def get_price(self):
        """gather price variations

        :return: current price, original price, discounted or not
        :rtype: float, float, str
        """
        current_price = self.product_data["units"][0]["displayPrice"]["price"]["value"]
        original_price = self.product_data["units"][0]["displayPrice"]["originalPrice"]["value"]
        discounted = self.product_data["units"][0]["displayPrice"]["isDiscounted"]
        return current_price, original_price, discounted

    def get_currency(self):
        """gather currency

        :return: currency
        :rtype: str
        """
        return self.product_data["units"][0]["displayPrice"]["price"]["currency"]

    def get_images(self):
        """gather list of image urls

        :return: image urls
        :rtype: list
        """
        image_lst = self.product_data["media"]["images"]
        return [x["sources"]["zoom"] for x in image_lst]

    def get_reviews(self):
        """gather number of reviews and average rating if available

        :return: review count, average rating
        :rtype: int, float
        """
        return int(self.product_data["reviewsCount"]), float(self.product_data["averageStarRating"])

    def get_data(self):
        """calls get_data_main() to gather all data

        :return: scraped data
        :rtype: dict
        """
        return get_data_main(self)


class HM:
    """Class to scrape H&M data"""
    def __init__(self, url):
        """sets url and calls __fetch_page()

        :param url: url of product to scrape data from
        """
        self.url = url
        self.product_data, self.product_details = self.__fetch_page()

    def __fetch_page(self):
        """gets product data via webdriver access

        :return: product data, product details
        :rtype: dict, dict
        """
        driver = webdriver.Chrome()
        driver.get(self.url)
        product_data = driver.execute_script("return document.getElementById('product-schema').textContent")
        product_details = driver.execute_script("return productArticleDetails[hm.product.getArticleId()]")
        driver.close()
        return json.loads(product_data), product_details

    def get_article_id(self):
        """gather article id

        :return: article id
        :rtype: str
        """
        return self.product_data["sku"]

    def get_title(self):
        """gather title

        :return: title
        :rtype: str
        """
        return self.product_data["name"]

    def get_brand(self):
        """gather brand name

        :return: brand name
        :rtype: str
        """
        return self.product_data["brand"]["name"]

    def get_category(self):
        """gather category

        :return: category
        :rtype: str
        """
        return self.product_data["category"]["name"]

    def get_target_gender(self):
        """gather target gender

        :return: gender
        :rtype: str
        """
        return None

    def get_color(self):
        """gather color

        :return: color
        :rtype: str
        """
        return self.product_data["color"]

    def get_description(self):
        """gather description

        :return: description
        :rtype: str
        """
        return self.product_data["description"]

    def get_price(self):
        """gather price variations

        :return: current price, original price, discounted or not
        :rtype: float, float, str
        """
        current_price = self.product_data["offers"][0]["price"]
        original_price = current_price
        discounted = False
        return current_price, original_price, discounted

    def get_currency(self):
        """gather currency

        :return: currency
        :rtype: str
        """
        return self.product_data["offers"][0]["priceCurrency"]

    def get_images(self):
        """gather list of image urls

        :return: image urls
        :rtype: list
        """
        return [x["image"] for x in self.product_details["images"]]

    def get_reviews(self):
        """gather number of reviews and average rating if available

        :return: review count, average rating
        :rtype: int, float
        """
        return None, None

    def get_data(self):
        """calls get_data_main() to gather all data

        :return: scraped data
        :rtype: dict
        """
        return get_data_main(self)


class ASOS:
    """Class to scrape ASOS data"""
    def __init__(self, url):
        """sets url and calls __fetch_page()

        :param url: url of product to scrape data from
        """
        self.url = url
        self.product_data = self.__fetch_page()

    def __fetch_page(self):
        """gets product data via webdriver access

        :return: product data
        :rtype: dict
        """
        driver = webdriver.Chrome()
        driver.get(self.url)
        product_data = json.loads(driver.execute_script("return JSON.stringify(window.asos.pdp)"))
        driver.close()
        return product_data

    def get_article_id(self):
        """gather article id

        :return: article id
        :rtype: str
        """
        return self.product_data["config"]["product"]["id"]

    def get_title(self):
        """gather title

        :return: title
        :rtype: str
        """
        return self.product_data["config"]["product"]["name"]

    def get_brand(self):
        """gather brand name

        :return: brand name
        :rtype: str
        """
        return self.product_data["config"]["product"]["brandName"]

    def get_category(self):
        """gather category

        :return: category
        :rtype: str
        """
        return self.product_data["config"]["product"]["productType"]["name"]

    def get_target_gender(self):
        """gather target gender

        :return: gender
        :rtype: str
        """
        return self.product_data["config"]["product"]["gender"]

    def get_color(self):
        """gather color

        :return: color
        :rtype: str
        """
        return self.product_data["config"]["product"]["variants"][0]["colour"]

    def get_description(self):
        """gather description

        :return: description
        :rtype: str
        """
        return None

    def get_price(self):
        """gather price variations

        :return: current price, original price, discounted or not
        :rtype: float, float, str
        """
        current_price = float(self.product_data["stockPrice"][0]["productPrice"]["current"]["value"])
        original_price = self.product_data["stockPrice"][0]["productPrice"]["rrp"]["value"]
        if original_price:
            original_price = float(original_price)
        else:
            original_price = current_price
        discounted = self.product_data["stockPrice"][0]["productPrice"]["isOutletPrice"]
        return current_price, original_price, discounted

    def get_currency(self):
        """gather currency

        :return: currency
        :rtype: str
        """
        return self.product_data["stockPrice"][0]["productPrice"]["currency"]

    def get_images(self):
        """gather list of image urls

        :return: image urls
        :rtype: list
        """
        return [x["url"] for x in self.product_data["config"]["product"]["images"]]

    def get_reviews(self):
        """gather number of reviews and average rating if available

        :return: review count, average rating
        :rtype: int, float
        """
        return None, None

    def get_data(self):
        """calls get_data_main() to gather all data

        :return: scraped data
        :rtype: dict
        """
        return get_data_main(self)


class SheIn:
    """Class to scrape SheIn data"""
    def __init__(self, url):
        """sets url and calls __fetch_page()

        :param url: url of product to scrape data from
        """
        self.url = url
        self.product_data = self.__fetch_page()

    def __fetch_page(self):
        """gets product data via webdriver access

        :return: product data
        :rtype: dict
        """
        driver = webdriver.Chrome()
        driver.get(self.url)
        product_data = json.loads(driver.execute_script("return JSON.stringify("
                                                        "window.goodsDetailv2SsrData.productIntroData)"))
        driver.close()
        return product_data

    def get_article_id(self):
        """gather article id

        :return: article id
        :rtype: str
        """
        return self.product_data["detail"]["goods_id"]

    def get_title(self):
        """gather title

        :return: title
        :rtype: str
        """
        return self.product_data["detail"]["goods_name"]

    def get_brand(self):
        """gather brand name

        :return: brand name
        :rtype: str
        """
        return self.product_data["detail"]["brand"]

    def get_category(self):
        """gather category

        :return: category
        :rtype: str
        """
        return self.product_data["currentCat"]["cat_name"]

    def get_target_gender(self):
        """gather target gender

        :return: gender
        :rtype: str
        """
        return self.product_data["parentCats"]["cat_name"]

    def get_color(self):
        """gather color

        :return: color
        :rtype: str
        """
        prod_details = self.product_data["detail"]["productDetails"]
        for e in prod_details:
            if e["attr_name_en"] == "Color":
                return e["attr_value_en"]

    def get_description(self):
        """gather description

        :return: description
        :rtype: str
        """
        return self.product_data["detail"]["goods_desc"].replace("\n", ", ")

    def get_price(self):
        """gather price variations

        :return: current price, original price, discounted or not
        :rtype: float, float, str
        """
        current_price = float(self.product_data["detail"]["salePrice"]["amount"])
        original_price = float(self.product_data["detail"]["retailPrice"]["amount"])
        discounted = True
        if int(self.product_data["detail"]["unit_discount"]) == 0:
            discounted = False
        return current_price, original_price, discounted

    def get_currency(self):
        """gather currency

        :return: currency
        :rtype: str
        """
        return ''.join([x for x in self.product_data["detail"]["retailPrice"]["amountWithSymbol"] if not x.isdigit()
                        and x not in [",", "."]])

    def get_images(self):
        """gather list of image urls

        :return: image urls
        :rtype: list
        """
        return [x["origin_image"] for x in self.product_data["goods_imgs"]["detail_image"]]

    def get_reviews(self):
        """gather number of reviews and average rating if available

        :return: review count, average rating
        :rtype: int, float
        """
        return None, None

    def get_data(self):
        """calls get_data_main() to gather all data

        :return: scraped data
        :rtype: dict
        """
        return get_data_main(self)


class Revolve:
    """Class to scrape Revolve data"""
    def __init__(self, url):
        """sets url and calls __fetch_page()

        :param url: url of product to scrape data from
        """
        self.url = url
        self.product_data = self.__fetch_page()

    def __fetch_page(self):
        """gets product data via webdriver access

        :return: product data
        :rtype: dict
        """
        driver = webdriver.Chrome()
        driver.get(self.url)
        product_data = json.loads(driver.execute_script("return document.getElementsByTagName('body')"
                                                        "[0].getElementsByTagName('script')[0].textContent"))
        driver.close()
        return product_data

    def get_article_id(self):
        """gather article id

        :return: article id
        :rtype: str
        """
        return self.product_data["sku"]

    def get_title(self):
        """gather title

        :return: title
        :rtype: str
        """
        return self.product_data["name"]

    def get_brand(self):
        """gather brand name

        :return: brand name
        :rtype: str
        """
        return self.product_data["brand"]["name"]

    def get_category(self):
        """gather category

        :return: category
        :rtype: str
        """
        return None

    def get_target_gender(self):
        """gather target gender

        :return: gender
        :rtype: str
        """
        return "Women"

    def get_color(self):
        """gather color

        :return: color
        :rtype: str
        """
        return None

    def get_description(self):
        """gather description

        :return: description
        :rtype: str
        """
        return self.product_data["description"]

    def get_price(self):
        """gather price variations

        :return: current price, original price, discounted or not
        :rtype: float, float, str
        """
        current_price = float(self.product_data["offers"]["price"])
        original_price = current_price
        discounted = False
        return current_price, original_price, discounted

    def get_currency(self):
        """gather currency

        :return: currency
        :rtype: str
        """
        return self.product_data["offers"]["priceCurrency"]

    def get_images(self):
        """gather list of image urls

        :return: image urls
        :rtype: list
        """
        return [self.product_data["image"]]

    def get_reviews(self):
        """gather number of reviews and average rating if available

        :return: review count, average rating
        :rtype: int, float
        """
        review_count = self.product_data["aggregateRating"]["reviewCount"]
        avrg_rating = self.product_data["aggregateRating"]["ratingValue"]
        return review_count, avrg_rating

    def get_data(self):
        """calls get_data_main() to gather all data

        :return: scraped data
        :rtype: dict
        """
        return get_data_main(self)
