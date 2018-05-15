# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbPt1Item(scrapy.Item):
	title = scrapy.Field()
	imdb_rating = scrapy.Field()
	meta_rating = scrapy.Field()
	genre = scrapy.Field()
	run_time = scrapy.Field()
	gross = scrapy.Field()