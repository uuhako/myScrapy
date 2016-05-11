#!/usr/bin/python
#encoding=utf-8

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from items import articleItem

class ItSpider(scrapy.Spider):
    name = 'ItSpider'
    allowed_domains = ['cnbeta.com']
    start_urls = ['http://www.cnbeta.com']

    def parse(self, response):
        for article in response.css('#allnews_all .title'):
            href = article.css('a::attr(href)')
            full_url = response.urljoin(href[0].extract())
#             yield scrapy.Request(full_url, callback=self.parse_item)
            yield self.parse_from_mainpage(article, response)

    def parse_from_mainpage(self, article, response):
        href = article.css('a::attr(href)')
        full_url = response.urljoin(href[0].extract())
        item = articleItem()
        item['title'] = article.css('a::text')[0].extract().encode('gbk')
        item['link'] = full_url
        item['src'] = None
        item['pubDate'] = article.css('span > em::text')[0].extract()
        return item
        
    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)       
        item = articleItem()
        item['title'] = response.xpath('//*[@id="news_title"]/text()')[0].extract().encode('gbk')
        item['link'] = response.url
        item['src'] = response.xpath('//*[@class="where"]/a/text()')[0].extract().encode('gbk')
        item['pubDate'] = response.xpath('//*[@class="date"]/text()')[0].extract().encode('gbk')
        return item