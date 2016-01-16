import scrapy
from tutorial.items import TutorialItem

class BwogSpider(scrapy.Spider):
	name = 'bwog'
	allowed_domains = ['bwog.com']
	start_urls = ['http://bwog.com/']

	def parse(self, response):
		for section in response.xpath('//div[@class="blog-section"]'):
			link = section.xpath('.//a/@href').extract()[0]
			yield scrapy.Request(link, callback=self.parse_entry)
		next = response.xpath('//div[@class="comnt-btn"]//@href').extract()[0]
		yield scrapy.Request(next, callback=self.parse)

	def parse_entry(self, response):
		for comment in response.xpath('//div[@class="reg-comment-body "]'):
			paragraphs = comment.xpath('.//text()').extract()
			text = '\n'.join(paragraphs).strip()
			item = TutorialItem()
			item['content'] = text
			yield item
