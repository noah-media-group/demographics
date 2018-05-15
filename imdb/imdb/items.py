# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
	title = scrapy.Field()
	# imdb_rating = scrapy.Field()
	# meta_rating = scrapy.Field()
	# genre = scrapy.Field()
	release_date = scrapy.Field()
	MPAA_rating = scrapy.Field()
	# run_time = scrapy.Field()
	director = scrapy.Field()
	actors = scrapy.Field()
	male_teen_rating = scrapy.Field()
	male_youngAdult_rating = scrapy.Field()
	male_adult_rating = scrapy.Field()
	male_elder_rating = scrapy.Field()
	male_ratingCount = scrapy.Field()
	# male_teen_ratingCount = scrapy.Field()
	# male_youngAdult_ratingCount = scrapy.Field()
	# male_adult_ratingCount = scrapy.Field()
	# male_elder_ratingCount = scrapy.Field()
	female_teen_rating = scrapy.Field()
	female_youngAdult_rating = scrapy.Field()
	female_adult_rating = scrapy.Field()
	female_elder_rating = scrapy.Field()
	female_ratingCount = scrapy.Field()
	# female_teen_ratingCount = scrapy.Field()
	# female_youngAdult_ratingCount = scrapy.Field()
	# female_adult_ratingCount = scrapy.Field()
	# female_elder_ratingCount = scrapy.Field()
	non_USusers = scrapy.Field()
	# non_UScount = scrapy.Field()
	us_users = scrapy.Field()
	# us_count = scrapy.Field()
	