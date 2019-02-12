# -*- coding: utf-8 -*-

##############################
# GET A REQUEST FOR EACH PAGE, FOR EACH PAGE, ESTABLISH NEW SON REQUESTS FOR NEW LINKS. 
# WHEN ALL SON REQUESTS DONE, GO TO THE NEXT PAGE

import scrapy
import re,sys

regx = re.compile(r'百度网盘密码：([0-9a-zA-Z]{4})')
fh = open('log.txt', 'w')


class Imdb_son_requestSpider(scrapy.Spider):
	name = 'mebook.py'
	start_urls = ['http://mebook.cc/page/1']
	
	custom_settings = {
			'FEED_FORMAT' : 'csv',
			'FEED_URI' : '/ifs4/BC_RD/USER/wangguangya/Pyscripts/scrapy/qoutes/qoutes/spiders/mebook.csv',
			}
	def parse(self, response):
		for item in response.css('div.img a::attr(href)').extract():               # get href link then another request to that page
			#print(item)
			#if not item:
			#	sys.exit("SHUT DOWN EVERYTHING!")
			yield response.follow(item, self.parse_down_btn)                             # this place many links can be parsed,the use corresponding parse function to get contents
			
		for i in range(2,834):
			page = 'http://mebook.cc/page/' + str(i)
			yield response.follow(page, self.parse)

	
	def parse_book(self, response):
		bookpage = response.css('div.img a::attr(href)').extract_first()
		#if not bookpage:
		#	sys.exit("SHUT DOWN EVERYTHING!")
		yield response.follow(bookpage, self.parse_down_btn)                                                                    
		fh.write(bookpage)
		fh.flush()
	
	def parse_down_btn(self, response):
		down_btn = response.css('a.downbtn').xpath('@href').extract_first()
		#if not down_btn:
		#	sys.exit("SHUT DOWN EVERYTHING!")
		yield response.follow(down_btn, self.parse_baidu)

	def parse_baidu(self, response):
		baidu_pwd_str = response.css('body div.desc p:contains("网盘密码")').extract_first()
		rematch = regx.search(baidu_pwd_str)
		baidu_pwd = rematch.group(1)
		baidu_link = response.css('div.list a:contains("百度网盘")').xpath('@href').extract_first()
		title = response.css('h1 a::text').extract_first().strip()
		#if not (baidu_pwd and baidu_link and title):
		#	sys.exit("SHUT DOWN EVERYTHING!")
		yield{
			'title':title,
			'baidu_link':baidu_link,
			'baidu_pwd':baidu_pwd
		}
