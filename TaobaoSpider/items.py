# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProductItem(scrapy.Item):
    nid = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    raw_title = scrapy.Field()
    pic_url = scrapy.Field()
    view_fee = scrapy.Field()
    item_loc = scrapy.Field()
    view_sales = scrapy.Field()
    comment_count = scrapy.Field()
    user_id = scrapy.Field()
    nick = scrapy.Field()
    keyword = scrapy.Field()


class CommentItem(scrapy.Item):
    pass

