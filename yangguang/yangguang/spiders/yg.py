# -*- coding: utf-8 -*-
import scrapy
import re
from yangguang.items import YangguangItem


class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://d.wz.sun0769.com/index.php/question/questionType']

    def parse(self, response):
        tr_list = response.xpath('''//div[@class="greyframe"]/table[2]/tr/td/table/tr''')
        for tr in tr_list:
            item = YangguangItem()
            item['title'] = tr.xpath('''./td[2]/a[@class="news14"]/text()''').extract_first()
            item['href'] = tr.xpath('''./td[2]/a[@class="news14"]/@href''').extract_first()
            item['update_time'] = tr.xpath('''./td[@class="t12wh"]/text()''').extract_first()
            next_url = str(item['href'])
            # print(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_detail,
                meta={"item": item},
                dont_filter=False
            )
        # 翻页
        url = response.xpath('''//a[text()=">"]/@href''').extract_first()
        print(url)
        if url != None:
            yield scrapy.Request(
                str(url),
                callback=self.parse,
                # dont_filter=False
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['detail'] = response.xpath('''//div[@class="wzy1"]/table[2]/tr[1]//text()''').extract()
        # print(item)
        yield item
