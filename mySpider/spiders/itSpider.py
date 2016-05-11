#!/usr/bin/python
#encoding=utf-8

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from items import articleItem

class ItSpider(CrawlSpider):
    name = 'ItSpider'
    allowed_domains = ['cnbeta.com']
    start_urls = ['http://www.cnbeta.com']

    rules = (
#         Rule(LinkExtractor(allow=('/article/', ))),

        Rule(LinkExtractor(allow=('article', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        
#         print response.xpath('//*[@id="news_title"]/text()')[0].extract()
#         
        item = articleItem()
        item['title'] = response.xpath('//*[@id="news_title"]/text()')[0].extract().encode('gbk')
        print item['title']
        item['link'] = None
        item['src'] = None
        item['pubDate'] = None
#         print item
        return item