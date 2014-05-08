from scrapy.spider import Spider
from scrapy.selector import Selector

class DmozSpider(Spider):
	name = "taioanchouhap"
	allowed_domains = ["taioanchouhap.pixnet.net",
					   'taioan-chouhap.myweb.hinet.net']
	start_urls = [
		"http://taioanchouhap.pixnet.net/blog",
		"http://taioan-chouhap.myweb.hinet.net/0_boklok.htm",
		'http://taioanchouhap.pixnet.net/blog/post/177926499',
	]
	
	def parse(self, response):
		filename = response.url.replace("/", '_')
		open(filename, 'wb').write(response.body)
		
		sel = Selector(response)
		for url in sel.xpath('//a/@href').extract():
			print(url)
		
