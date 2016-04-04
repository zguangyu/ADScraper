# -*- coding: utf-8 -*-
import re
import scrapy

from ADScraper.items import ADItem

class AdscrapySpider(scrapy.Spider):
    name = "adscraper"
    allowed_domains = ["analog.com"]
    start_urls = [
        "http://www.analog.com/cn/products.html",
    ]

    def parse(self, response):
        for href in response.xpath("//a[contains(@href, 'products/')]/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_subpage)

    def parse_subpage(self, response):
        if response.xpath("//table"):
            for href in response.xpath("//table//tr/td[1]/a[1]/@href"):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_item)
            return

        url_prefix = response.url.replace(".html", "/")

        for href in response.xpath("//a[contains(@href, '%s')]/@href" % url_prefix):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_subpage)


    def parse_item(self, response):
        item = ADItem()
        item['name'] = response.xpath("//h1[@itemprop='name']/text()").extract()[0]
        item['url'] = response.url

        if response.css(u"a[name*='中文数据手册']::attr(href)"):
            item['zh_data_manual'] = response.urljoin(response.css(u"a[name*='中文数据手册']::attr(href)").extract()[0])

        if response.css(u"a[name*='英文数据手册']::attr(href)"):
            item['en_data_manual'] = response.urljoin(response.css(u"a[name*='英文数据手册']::attr(href)").extract()[0])

        if response.css(u"a[name*='用户手册']::attr(href)"):
            item['user_manual'] = response.urljoin(response.css(u"a[name*='用户手册']::attr(href)").extract()[0])

        yield item
