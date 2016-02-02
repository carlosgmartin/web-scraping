import scrapy
from myproject.items import MyItem

class MySpider(scrapy.Spider):
    name = 'myspider'
    allowed_domains = ['bwog.com']
    start_urls = ['http://bwog.com']

    def parse(self, response):
        for section in response.xpath('//div[@class="blog-section"]'):
            link = section.xpath('.//a/@href').extract()[0]
            yield scrapy.Request(link, callback=self.parse_entry)
        next = response.xpath('//div[@class="comnt-btn"]//@href').extract()[0]
        yield scrapy.Request(next, callback=self.parse)

    def parse_entry(self, response):
        for comment in response.xpath('//div[contains(@class, " comment-body")]'):
            item = MyItem()

            item['author'] = comment.xpath('./div[@class="comment-author vcard"]/cite/text()').extract_first()

            metadata = comment.xpath('./div[@class="comment-meta datetime"]')
            item['up'] = int(metadata.xpath('./span[@data-voting-direction="up"]/span/text()').extract_first())
            item['down'] = int(metadata.xpath('./span[@data-voting-direction="down"]/span/text()').extract_first())
            item['datetime'] = metadata.xpath('./a/text()').extract_first().strip()

            paragraphs = comment.xpath('./div[contains(@class, "reg-comment-body")]/p/text()').extract()
            item['content'] = '\n'.join(paragraphs)

            yield item