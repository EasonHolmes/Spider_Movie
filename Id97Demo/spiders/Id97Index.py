# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from Id97Demo.items import Id97DemoItem
import re


class Id97Movie(CrawlSpider):
    name = 'id97'
    host = 'http://www.id97.com'
    allowed_domains = ['www.id97.com']
    start_urls = ['http://www.id97.com/movie']

    def parse(self, response):
        selector = Selector(response)
        divs = selector.xpath("//div[@class='col-xs-1-5 col-sm-4 col-xs-6 movie-item']")
        pages = selector.xpath("body/div/div[@class='pager-bg']/ul/li")

        for div in divs:
            yield self.parse_item(div)

        nextPageUrl = self.host + (pages[- 2].xpath('a/@href').extract_first())
        yield Request(nextPageUrl, callback=self.parse)

    def parse_item(self, div):
        item = Id97DemoItem()
        item['articleUrl'] = div.xpath('div[@class="movie-item-in"]/a/@href').extract_first()
        item['movieName'] = div.xpath('div[@class="movie-item-in"]/a/@title').extract_first()

        score = div.xpath('div[@class="movie-item-in"]/div[@class="meta"]/h1/em/text()').extract_first()
        item['scoreNumber'] = self.convertScore(score)

        # 用string包裹标签就能获取该标签下的所有文字包括子标签的
        style = div.xpath(
            'string(div[@class="movie-item-in"]/div[@class="meta"]/div[@class="otherinfo"])').extract_first(
            default="")
        item['style'] = style

        return item

    # 获取字符串中的数字
    def convertScore(self, str):
        list = re.findall(r"\d+\.?\d*", str)
        if list:
            return list.pop(0)
        else:
            return 0
