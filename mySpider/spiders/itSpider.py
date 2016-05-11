#!/usr/bin/python
#encoding=utf-8

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from items import articleItem
import json

class ItSpider(scrapy.Spider):
    name = 'ItSpider'
#     start_urls = ['http://www.cnbeta.com']

    def start_requests(self):
        requests = []
        import os,sys
        rootFolder = os.path.dirname(__file__)
        sys.path.append(rootFolder)
        path = rootFolder + '/../input/sites.json'
        try:
            fd = open(path, 'r+b')
        except Exception as e:
            print 'open file failed'
            raise e;
#         requests.append()
        data = fd.read()
        sites = json.loads(data)
        for config in sites["sites"]:
            if config["enabled"] == "True":
                requests.append(Request(url = config["url"], meta=config))
        return requests
        
    def parse(self, response):
        config = response.meta
        for href in response.xpath(config["xpath_article"]):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_article, meta=config)
#             yield self.parse_from_mainpage(article, response)

    def parse_from_mainpage(self, article, response):
        href = article.css('a::attr(href)')
        full_url = response.urljoin(href[0].extract())
        item = articleItem()
        item['title'] = article.css('a::text')[0].extract().encode('gbk')
        item['link'] = full_url
        item['where'] = None
        item['pubDate'] = article.css('span > em::text')[0].extract()
        return item
        
    def parse_article(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        config = response.meta      
        item = articleItem()
        item['title'] = response.xpath(config["xpath_title"])[0].extract().encode('gbk')
        item['link'] = response.url
        if config["xpath_where"] != []:
            where = response.xpath(config["xpath_where"][0])
            if where != []:
                item['where'] = where[0].extract().encode('gbk')
                item['where_link'] = response.xpath(config["xpath_where_link"])[0].extract().encode('gbk')
            else:
                where = response.xpath(config["xpath_where"][1])
                if where != []:
                    item['where'] = where[0].extract().replace(config["where_replacer"], "").encode('gbk')
        else:
            item['where'] = config['name'].encode('gbk')

        item['pubDate'] = response.xpath(config["xpath_pubDate"])[0].extract().encode('gbk')
        
        if item["where"].lower() != config["name"].encode('gbk').lower():
            return None
        return item
    
    