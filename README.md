# WebscrapingClothingShops

WebscrapingClothingShops is Python project to scrape product data of Online Clothing Stores.  
The online shops Zalando, H&M, ASOS, SheIn and Revolve are currently supported.

## Requirements

Selenium WebDriver has to be installed. A detailed description on how to install Selenium can be found [here](https://selenium-python.readthedocs.io/installation.html).  
Furthermore a driver, e.g. chromedriver or geckodriver, has to be installed and has to be in PATH. A guide for this process can be found [here](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/).

## Usage

```python
from ScrapingShops import Zalando, HM, ASOS, SheIn, Revolve

item = Zalando("url-to-zalando-product")

item.get_article_id() # returns article id
item.get_title() # return title
item.get_brand() # returns brand name
item.get_category() # returns category
item.get_target_gender() # returns target gender
item.get_color() # returns color
item.get_description() # returns description
item.get_price() # returns prices
item.get_currency() # returns currency
item.get_images() # returns image urls

item.get_data() # returns all data

```

## What I Learned
- Usage of Python classes
- Fetch webpage data using Selenium
