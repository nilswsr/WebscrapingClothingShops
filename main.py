import json
from clothing import ZalandoScraping, HMScraping

"""
zalando_item = ZalandoScraping("https://www.zalando.de/bronx-jaxstar-schnuerstiefel-cappuccino-br111a07a-b11.html")
zalando_data = zalando_item.get_data()
zalando_json = json.dumps(zalando_data, indent=2, ensure_ascii=False)
print(zalando_json)
"""


hm_item = HMScraping("https://www2.hm.com/de_de/productpage.0950532001.html")
hm_data = hm_item.get_data()
hm_json = json.dumps(hm_data, indent=2, ensure_ascii=False)
print(hm_json)