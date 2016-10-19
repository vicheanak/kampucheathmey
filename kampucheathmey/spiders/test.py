# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from kampucheathmey.items import KampucheathmeyItem
from scrapy.linkextractors import LinkExtractor
import time
import lxml.etree
import lxml.html


class TestSpider(CrawlSpider):
    name = "kampucheathmey"
    allowed_domains = ["kampucheathmey.com"]
    start_urls = [
    'http://kampucheathmey.com/2016/ព័ត៌មានជាតិ/ព័ត៌មានជាតិទូទៅ',
    ]

    def parse(self, response):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        hxs = scrapy.Selector(response)

        articles = hxs.xpath('//div[@class="feature-post-list"]')

        for article in articles:
            item = KampucheathmeyItem()
            item['categoryId'] = '1'
            name = article.xpath('div[@class="post_loop_content"][1]/h3[1]/a[1]/text()')
            if not name:
                print('Kampucheathmey => [' + now + '] No title')
            else:
                item['name'] = name.extract_first()

            url = article.xpath('div[@class="post_loop_content"][1]/h3[1]/a[1]/@href')
            if not url:
                print('Kampucheathmey => [' + now + '] No url')
            else:
                item['url'] = url.extract_first()

            description = article.xpath('div[@class="post_loop_content"][1]/p[@class="post_des"][1]/text()')
            if not description:
                print('Kampucheathmey => [' + now + '] No description')
            else:
                item['description'] = description.extract_first()


            request = scrapy.Request(item['url'], callback=self.parse_detail)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        item = response.meta['item']
        hxs = scrapy.Selector(response)
        now = time.strftime('%Y-%m-%d %H:%M:%S')


        imageUrl = hxs.xpath("""
            //div[@class="single_post_format_image"]/img[1]/@src
            """)
        item['imageUrl'] = ''
        if not imageUrl:
            print('Kampucheathmey => [' + now + '] No imageUrl')
        else:
            item['imageUrl'] = imageUrl.extract_first()

        root = lxml.html.fromstring(response.body)
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")
        htmlcontent = ''

        for p in root.xpath('//div[@class="post_content"][1]'):
            htmlcontent = lxml.html.tostring(p, pretty_print=True, encoding=unicode)

        item['htmlcontent'] = htmlcontent


        yield item
