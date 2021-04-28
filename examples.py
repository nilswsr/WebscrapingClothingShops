from ScrapingShops import Zalando, HM, ASOS, SheIn, Revolve

# new instance of class Zalando with url of wanted product
item = Zalando("https://www.zalando.co.uk/nike-sportswear-basic-t-shirt-black-ni122o0nk-q11.html")

# Article ID of item
article_id = item.get_article_id()

# Title of item
title = item.get_title()

# Brand name of item
brand_name = item.get_brand()

# Category of item
category = item.get_category()

# Target gender of item
gender = item.get_target_gender()

# Color of item
color = item.get_color()

# Description of item
description = item.get_description()

# Current price, regular price and if item is discounted or not
current_price, original_price, discounted = item.get_price()

# Currency of price
currency = item.get_currency()

# Image urls of item
images = item.get_images()

# All data combined in dictionary
data = item.get_data()
