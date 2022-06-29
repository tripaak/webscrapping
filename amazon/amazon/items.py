# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def strip_string(value):
    return value.strip()

def replace(value):
    return value.replace('€', '')    


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(input_processor= MapCompose(remove_tags, strip_string), output_processor=TakeFirst())
    review = scrapy.Field(input_processor= MapCompose(remove_tags, strip_string), output_processor=TakeFirst())
    price = scrapy.Field(input_processor= MapCompose(remove_tags, replace, strip_string), output_processor=TakeFirst())
    
