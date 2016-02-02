import scrapy

class MyItem(scrapy.Item):
    author = scrapy.Field()
    up = scrapy.Field()
    down = scrapy.Field()
    datetime = scrapy.Field()
    content = scrapy.Field()