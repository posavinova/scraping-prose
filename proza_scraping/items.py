# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import datetime
from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy.item import Item, Field


def convert_date_datetime(date_raw):
    date = datetime.datetime.strptime(date_raw[2:], '%d.%m.%Y %H:%M')
    return date


def normalize_link(link):
    link = "https://proza.ru" + link
    return link


def normalize_text(text):
    extra = ["\xa0", "\t"]
    for symbol in extra:
        if symbol in text:
            text = text.replace(symbol, " ").strip()
    return text


class StoriesItem(Item):
    title = Field(output_processor=TakeFirst())
    link = Field(input_processor=MapCompose(normalize_link), output_processor=TakeFirst())
    author = Field(output_processor=TakeFirst())
    author_link = Field(input_processor=MapCompose(normalize_link), output_processor=TakeFirst())
    date = Field(input_processor=MapCompose(convert_date_datetime), output_processor=TakeFirst())
    text = Field(input_processor=MapCompose(normalize_text), output_processor=Join())
