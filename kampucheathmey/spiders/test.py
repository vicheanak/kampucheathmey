# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from kampucheathmey.items import KampucheathmeyItem
from scrapy.linkextractors import LinkExtractor
import time


class TestSpider(CrawlSpider):
    name = "kampucheathmey"
    allowed_domains = ["kampucheathmey.com"]
    start_urls = [
    'https://kampucheathmey.com/2016/ព័ត៌មានជាតិ/ព័ត៌មានជាតិទូទៅ',
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

            imageUrl = article.xpath("""
                div[@class="image_post feature-item loadmore_list_image"]/a[1]/img[1]/@src
                """)

            item['imageUrl']
            if not imageUrl:
                print('Kampucheathmey => [' + now + '] No imageUrl')
            else:
                item['imageUrl'] = imageUrl.extract_first()

            yield item

    def parse_detail(self, response):
        item = response.meta['item']
        hxs = scrapy.Selector(response)
        now = time.strftime('%Y-%m-%d %H:%M:%S')

        item_page = hxs.css('div.item-page')
        description = item_page.xpath('p[1]/text()')
        if not description:
            print('Kampucheathmey => [' + now + '] No description')
        else:
            item['description'] = item_page.xpath('p[1]/strong/text()').extract_first() + ' ' + description.extract_first()

        imageUrl = item_page.xpath('p[last()]/img/@src')
        if not imageUrl:
            print('Kampucheathmey => [' + now + '] No imageUrl')
        else:
            item['imageUrl'] = imageUrl.extract_first()


        yield item
