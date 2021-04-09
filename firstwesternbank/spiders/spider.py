import scrapy

from scrapy.loader import ItemLoader

from ..items import FirstwesternbankItem
from itemloaders.processors import TakeFirst


class FirstwesternbankSpider(scrapy.Spider):
	name = 'firstwesternbank'
	start_urls = ['https://www.firstwestern.bank/news-alerts/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="read-more"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next page-numbers"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//div[@class="post-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="date"]/text()').get()

		item = ItemLoader(item=FirstwesternbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
