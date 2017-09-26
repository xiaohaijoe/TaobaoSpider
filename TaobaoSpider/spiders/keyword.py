# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
import json
import pymongo

MONGO_URL = 'localhost'
MONGO_DB = 'TaobaoSpider'
MONGO_TABLE_PRODUCT = 'product'
MONGO_TABLE_COMMENT = 'comment'

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

keyword = '飞机杯'
class KeywordSpider(CrawlSpider):
    name = 'keyword'
    allowed_domains = ['taobao.com']
    start_urls = ['http://taobao.com/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    # keyword = ''
    # suggest_word = ''

    # url = 'https://s.taobao.com/search?data-key=s%2Cps&data-value=0%2C1&ajax=true&_ksTS=1506403406228_1114&callback=jsonp1115&ie=utf8&initiative_id=staobaoz_20170926&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E9%A3%9E%E6%9C%BA%E6%9D%AF%E7%94%B7%E7%94%A8&suggest=0_1&_input_charset=utf-8&wq=%E9%A3%9E%E6%9C%BA%E6%9D%AF&suggest_query=%E9%A3%9E%E6%9C%BA%E6%9D%AF&source=suggest&bcoffset=4&p4ppushleft=%2C48&s=44'

    def parse(self, response):
        for i in [0]:
            url = 'https://s.taobao.com/search?data-key=s&data-value='+ str(44 * i) +'&ajax=true&_ksTS=1506403406228_1114&callback=&ie=utf8&initiative_id=staobaoz_20170926&stats_click=search_radio_all%3A1&js=1&imgfile=&q='+ str(keyword) +'&suggest=0_1&_input_charset=utf-8&wq='+ str(keyword) +'&suggest_query='+ str(keyword) +'&source=suggest&bcoffset=4&p4ppushleft=%2C48&s=' + str(44 * (i + 1))
            # print(url)
            yield Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        # item = ProductItem()
        obj = json.loads(response.text)
        products = obj['mods']['itemlist']['data']['auctions']
        for prod in products:
            item = {
                'nid': prod['nid'],
                'category': prod['category'],
                'title': prod['title'],
                'raw_title': prod['raw_title'],
                'pic_url': prod['pic_url'],
                'view_fee': prod['view_fee'],
                'item_loc': prod['item_loc'],
                'view_sales': prod['view_sales'],
                'comment_count': prod['comment_count'],
                'user_id': prod['user_id'],
                'nick': prod['nick'],
                'keyword': keyword,
            }
            self.save_product(item)
            comment_url = 'https://rate.tmall.com/list_detail_rate.htm?itemId='+ item['nid'] +'&sellerId=' + item['user_id'] + '&order=1&currentPage=1&append=0&content=1&tagId=&posi=&_ksTS=1506443143070_1091&callback='
            yield Request(url=comment_url, meta={'nid': item['nid'], 'user_id': item['user_id']}, callback = self.parse_comment)

    def parse_comment(self, response):
        obj = json.loads(response.text)
        nid = response.meta['nid']
        sellerId = response.meta['user_id']
        comments = obj['rateDetail']['rateList']
        for comment in comments:
            item = {
                'nid': comment['nid'],
                'auctionSku': comment['auctionSku'],
                'sellerId': comment['sellerId'],            # 颜色选择
                'rateDate': comment['rateDate'],            # 评论时间
                'rateContent': comment['rateContent'],      # 评论内容
                'tradeEndTime': comment['tradeEndTime'],    # 交易结束时间
                'reply': comment['reply'],                  # 回复
                'gmtCreateTime': comment['gmtCreateTime'],  # 创建时间
                'displayUserNick': comment['displayUserNick'], # 昵称
                'commentId': comment['id'],                 # 评论ID？
                'pics': json.dumps(comment['pics']),        # 图片
                'userVipLevel': comment['userVipLevel'],    # 用户等级
            }
            self.save_comment(item)

        lastPage = obj['rateDetail']['paginator']
        nextPage = obj['rateDetail']['page'] + 1
        if nextPage <= lastPage:
            comment_url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=' + nid + '&sellerId=' + sellerId + '&order=1&currentPage=' + nextPage + '&append=0&content=1&tagId=&posi=&_ksTS=1506443143070_1091&callback='
            yield Request(url=comment_url, meta={'nid': nid, 'user_id': sellerId}, callback=self.parse_comment)

    def save_product(self, product):
        try:
            res = db[MONGO_TABLE_PRODUCT].find({'nid': product['nid']})
            if res.count() == 0 and db[MONGO_TABLE_PRODUCT].insert(product):
                print('存储到Product表成功', product)
            else:
                print('重复提交Product', product)
        except Exception:
            print('存储到Product失败', product)

    def save_comment(self, comment):
        try:
            res = db[MONGO_TABLE_COMMENT].find({'commentId': comment['commentId']})
            if res.count() == 0 and db[MONGO_TABLE_COMMENT].insert(comment):
                print('保存到Comment表成功', comment)
            else:
                print('重复提交Comment', comment)
        except Exception:
            print('存储到Comment失败', comment)




