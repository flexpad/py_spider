# -*- coding: utf-8 -*-
from ..items import JZBTopicItem, JZBPostItem
from ..settings import BASE_URL
import scrapy
import io
import sys
import re

class JZBSpider(scrapy.Spider):
    name = "JZB"
    allowed_domains = ["m.jzb.com"]
    start_urls = [
        "https://m.jzb.com/bbs/forum-943-1-3.html"
    ]
    topic = 0
    loop = 0
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
    def parse(self, response):
        print(response)
        for sel in  response.xpath("//*[@id='tab1']/div[2]/ul"):
            item = JZBTopicItem()
            list_item = sel.xpath("./li")
            for one_item in list_item:
                item['title'] = one_item.xpath("./a/p/text()[name(..)!='span'][normalize-space()]").extract()[0]
                item['link'] = one_item.xpath("./a/@href").extract()[0]
                item['author'] = one_item.xpath("./div[1]/div[1]/p/text()").extract()[0]
                item['uid'] = re.search(r'\d+', one_item.xpath("./div[1]/div[1]/p/span/@style").extract()[0]).group()
                item['reply'] = one_item.xpath("./div[1]/div[2]/p/span/text()").extract()[0]
                print('Processing the URL: ', item['link'], ' author = ', item['author'], ' avator = ', item['uid'],' replys = ', item['reply'], '\n')
                yield item
                yield scrapy.Request(BASE_URL + item['link'], callback=self.parse_article)
            JZBSpider.loop += 1
            print("Current URL: ", sel.xpath('//footer/a[contains(., "下一页")]/@href').extract()[0], "\n")
            if JZBSpider.loop >60:
                return
            else:
                if sel.xpath('//footer/a[contains(., "下一页")]/@href').extract():
                    yield scrapy.Request(BASE_URL + sel.xpath('//footer/a[contains(., "下一页")]/@href').extract()[0], callback=self.parse)
                    pass
        # yield scrapy.Request('https://m.jzb.com/bbs/thread-6360523-1-1.html', callback=self.parse_article)
    def parse_article(self, response):
            # response.body.decode("gb18030")
            JZBSpider.topic += 1
            detail = response.xpath("//body")
            page_item = JZBPostItem()
            page_item['title'] = detail.xpath('//article/h1/text()')[0].extract()
            # page_item['time'] = detail.xpath("//article/p/span[@class='tdate fl']/text()")[0].extract()
            page_item['link'] = response.url
            post_list = detail.xpath('//div[@class="list"]/ul/li')
            # page_item['image_urls'] = list(map(lambda url: BASE_URL + re.sub("_300.", "_1024.", url), post_list.xpath('.//img/@src').extract()))
            test_louzhu = detail.xpath('//div[@class="list"]/ul/li[@id="louzhu"]/ul/li[1]/a/span/text()').extract()
            page_item['louzhu'] = ''
            if test_louzhu:
                page_item['louzhu'] = detail.xpath('//div[@class="list"]/ul/li[@id="louzhu"]/ul/li[1]/a/span/text()').extract()[0]
            for one_item in post_list:
                item = JZBPostItem()
                item['title'] = page_item['title']
                item['link'] = page_item['link']
                item['louzhu'] = page_item['louzhu']
                item['image_urls'] = list(map(lambda url: BASE_URL + re.sub("_300.", "_1024.", url), one_item.xpath('.//img/@src').extract()))
                item['userinfo'] = one_item.xpath('./ul[@class="userinfo"]/li[1]/a/span/text()').extract()[0]
                item['userurl'] = BASE_URL + one_item.xpath('./ul[@class="userinfo"]/li[1]/a/@href').extract()[0]
                item_list = one_item.xpath('./p[not(contains(., "下载【家长帮APP】"))]').extract()
                item['lou'] = one_item.xpath('./ul[@class="userinfo"]/li[@class="fr"]/span/text()').extract()[0]
                print("post_list: ", one_item.xpath("./div[@class='time']/div/text()").extract()[0])
                item['posttime'] = one_item.xpath("./div[@class='time']/div/text()").extract()[0]
                # item['list'] = ''.join(item_list)
                item['post'] = ''
                for post_item in item_list:
                    item['post'] += post_item
                    # print(" == ", post_item, "\n")
                print("Count = ", JZBSpider.loop, "Tile = ", item["title"], "User: ", item['userinfo'], " URL: ", item['link'], " Post_time: ", item["posttime"], " Lou: ", item['lou'], "\n")
                print('Item is = ', item['post'], '\n')
                yield(item)
            if detail.xpath('//footer/a[contains(., "下一页")]/@href').extract():
                yield scrapy.Request(BASE_URL + detail.xpath('//footer/a[contains(., "下一页")]/@href').extract()[0], callback=self.parse_article)
                pass