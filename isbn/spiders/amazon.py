# -*- coding: utf-8 -*-
import scrapy
from isbn.items import IsbnLoader


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.cn"]
    custom_settings = {
        'COOKIES_ENABLED': True,
        'COOKIES_DEBUG': True,
        'DOWNLOAD_DELAY': 1,
        'DOWNLOADER_MIDDLEWARES': {
            'isbn.middlewares.RandomUserAgentMiddleware': 300,
        }
    }

    def __init__(self, isbn_list, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.isbn_list = isbn_list

    def start_requests(self):
        for isbn in self.isbn_list:
            url = f'https://www.amazon.cn/s/field-keywords={isbn}'
            yield scrapy.Request(url, meta={'isbn': isbn}, callback=self.parse)

    def parse(self, response):
        for div in response.xpath("//div[@class='s-item-container']"):
            url = div.xpath(".//a[contains(@class, 's-color-twister-title-link')]/@href").extract_first()
            print("url", url)
            if url:
                yield scrapy.Request(url=url, meta=response.meta, callback=self.parse_book_page)

    def parse_book_page(self, response):
        import isbnlib
        il = IsbnLoader(selector=response)
        il.add_xpath('title', ".//span[@id='productTitle' or @id='ebooksProductTitle']/text()")
        il.add_xpath('author', ".//span[@class='author notFaded']/a/text()")
        il.add_value('isbn', isbnlib.mask(response.meta['isbn']))
        il.add_xpath('publish', "//li[b/text()='出版社:']/text()")
        item = il.load_item()
        yield item


def from_file(filename):
    with open(filename) as f:
        url_list = f.readlines()
    return url_list


def main():
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    import re

    url_list = [
        # QQ 扫码得到的链接
        # "http://qm.qq.com/cgi-bin/result?r=9787302444060&p=i&v=7.0.1.407",
    ]
    # or from file
    url_list = set(url_list + from_file('list.txt'))
    isbn_list = [re.search('r=(\d*)', url).group(1) for url in url_list]
    print(isbn_list)
    settings = {**get_project_settings(), 'FEED_FORMAT': 'csv', 'FEED_URI': 'books.csv'}
    process = CrawlerProcess(settings)
    process.crawl(AmazonSpider, isbn_list)
    process.start()
    process.stop()

if __name__ == '__main__':
    main()
