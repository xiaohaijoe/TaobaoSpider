# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
import json

from TaobaoSpider.items import ProductItem


class KeywordSpider(CrawlSpider):
    name = 'keyword'
    allowed_domains = ['s.taobao.com']
    start_urls = ['http://s.taobao.com/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    # keyword = ''
    # suggest_word = ''

    # url = 'https://s.taobao.com/search?data-key=s%2Cps&data-value=0%2C1&ajax=true&_ksTS=1506403406228_1114&callback=jsonp1115&ie=utf8&initiative_id=staobaoz_20170926&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E9%A3%9E%E6%9C%BA%E6%9D%AF%E7%94%B7%E7%94%A8&suggest=0_1&_input_charset=utf-8&wq=%E9%A3%9E%E6%9C%BA%E6%9D%AF&suggest_query=%E9%A3%9E%E6%9C%BA%E6%9D%AF&source=suggest&bcoffset=4&p4ppushleft=%2C48&s=44'

    def parse(self, response):
        keyword = '飞机杯男用'
        suggest_word = '飞机杯'
        for i in range(0, 99):
            url = 'https://s.taobao.com/search?data-key=s&data-value='+ str(44 * i) +'&ajax=true&_ksTS=1506403406228_1114&callback=&ie=utf8&initiative_id=staobaoz_20170926&stats_click=search_radio_all%3A1&js=1&imgfile=&q='+ str(keyword) +'&suggest=0_1&_input_charset=utf-8&wq='+ str(suggest_word) +'&suggest_query='+ str(suggest_word) +'&source=suggest&bcoffset=4&p4ppushleft=%2C48&s=' + str(44 * (i + 1))
            # print(url)
            print(i)
            yield Request(url=url, callback=self.page)
        pass


    def page(self, response):
        item = ProductItem()
        obj = json.loads(response.text)
        products = obj['mods']['itemlist']['data']['auctions']
        for prod in products:
            item['nid'] = prod['nid']
            item['category'] = prod['category']
            item['title'] = prod['title']
            item['raw_title'] = prod['raw_title']
            item['pic_url'] = prod['pic_url']
            item['view_fee'] = prod['view_fee']
            item['item_loc'] = prod['item_loc']
            item['view_sales'] = prod['view_sales']
            item['comment_count'] = prod['comment_count']
            item['user_id'] = prod['user_id']
            item['nick'] = prod['nick']
            yield item
        # text = response.text[]

        # pass






