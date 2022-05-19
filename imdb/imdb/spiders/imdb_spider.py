from scrapy import Spider, Request
from imdb.items import ImdbItem
import re

class imdbSpider(Spider):
	name = 'imdb_spider'
	allowed_urls = ['https://www.imdb.com/']
	start_urls = ['https://www.imdb.com/search/title?title_type=feature&release_date=2000-01-01,2018-05-31&num_votes=10000,&countries=us&page=1&ref_=adv_nxt']

	def parse(self, response):
		
		#find total number of pages and movies
		pagination_section = response.xpath('//div[@class="desc"]/span/text()').extract()
		print(pagination_section)

		regex = '[(\d+,)]*\d+'
		pagination_section_regex_matches = re.findall(regex, pagination_section[2])
		print(pagination_section_regex_matches)

		pagination_section_clean = pagination_section_regex_matches[2].replace(',',"")
		print(pagination_section_clean)
		tot_titles = int(pagination_section_clean)

		page_items = response.css('.lister-item-index').xpath("text()").getall()
		print(page_items)

		pg1 = int(page_items[0][:-1])
		per_page = int(page_items[-1][:-1])

		number_pages = tot_titles//per_page + 1

		request_url = ['https://www.imdb.com/search/title?title_type=feature&release_date=2000-01-01,2018-05-31&num_votes=10000,&countries=us&page={}&ref_=adv_nxt'.format(x) for x in range(1,number_pages)]


		for url in request_url:
			yield Request(url=url, callback=self.parse_resultPage)

	def parse_resultPage(self, response):

		#scraping details on movie results page
		# movie_list = response.xpath('//div[@class ="lister-item-content"]')

		# for details in movie_list:
		# 	title = details.xpath('.//h3[@class="lister-item-header"]/a/text()').extract_first()
		# 	run_time = int(re.findall('\d+',details.xpath('.//span[@class="runtime"]/text()').extract_first())[0])
		# 	genre = details.xpath('.//span[@class="genre"]/text()').extract_first().strip()
		# 	imdb_rating = float(details.xpath('.//div[@class="inline-block ratings-imdb-rating"]/strong/text()').extract_first())
		# 	try:
		# 		meta_rating = int(details.xpath('.//div[@class="inline-block ratings-metascore"]/span/text()').extract_first())
		# 	except IndexError:
		# 		meta_rating = ""

		movie_urls = response.xpath('//h3[@class="lister-item-header"]/a/@href').extract()
		movie_urls = ['https://www.imdb.com' + url for url in movie_urls]

		for url in movie_urls:
			yield Request(url=url, callback=self.parse_moviePage)


	def parse_moviePage(self, response):

		# run_time = response.meta['run_time']
		# genre = response.meta['genre']
		# imdb_rating = response.meta['imdb_rating']
		# meta_rating = response.meta['meta_rating']

		#extracting info from actual movie page
		title = response.xpath('//h1[@itemprop="name"]/text()').extract_first().strip()
		MPAA_rating = response.xpath('//div[@class="subtext"]/text()').extract()[1].strip()
		release_date = response.xpath('//a[@title="See more release dates"]/text()').extract_first().strip()
		director = response.xpath('//span[@itemprop="director"]/a/span/text()').extract_first()
		actors = response.xpath('//span[@itemprop="actors"]/a/span/text()').extract_first()



		rating_url = response.xpath('//div[@class="imdbRating"]/a/@href').extract()
		rating_url = ['https://www.imdb.com' + url for url in rating_url]

		for url in rating_url:
			yield Request(url=url, callback=self.parse_review_page,
				meta={'title': title, 'MPAA_rating': MPAA_rating,
				'release_date': release_date, 'director': director,
				'actors': actors})

	def parse_review_page(self, response):

		# run_time = response.meta['run_time']
		# genre = response.meta['genre']
		# imdb_rating = response.meta['imdb_rating']
		# meta_rating = response.meta['meta_rating']
		title = response.meta['title']
		MPAA_rating = response.meta['MPAA_rating']
		release_date = response.meta['release_date']
		director = response.meta['director']
		actors = response.meta['actors']


		#extracting review info
		try:
			male_teen_rating = float(response.xpath('//div[@class="bigcell"]/text()').extract()[6])
		except ValueError:
			male_teen_rating = ""
		try:
			male_youngAdult_rating = float(response.xpath('//div[@class="bigcell"]/text()').extract()[7])
		except ValueError:
			male_youngAdult_rating = ""
		try:
			male_adult_rating = float(response.xpath('//div[@class="bigcell"]/text()').extract()[8])
		except ValueError:
			male_adult_rating = ""
		try:
			male_elder_rating = float(response.xpath('//div[@class="bigcell"]/text()').extract()[9])
		except ValueError:
			male_elder_rating = ""
		try:
			male_ratingCount = int(response.xpath('//div[@class="smallcell"]/a/text()').extract()[5].strip().replace(',',""))
		except IndexError:
			male_ratingCount = ""
		# try:	
		# 	male_teen_ratingCount = int(response.xpath('//div[@class="smallcell"]/a/text()').extract()[6].strip().replace(',',""))
		# except ValueError:
		# 	male_teen_ratingCount = ""
		# try:
		# 	male_youngAdult_ratingCount = int(response.xpath('//div[@class="smallcell"]/a/text()').extract()[7].strip().replace(',',""))
		# except ValueError:
		# 	male_youngAdult_ratingCount = ""
		# try:
		# 	male_adult_ratingCount = int(response.xpath('//div[@class="smallcell"]/a/text()').extract()[8].strip().replace(',',""))
		# except ValueError:
		# 	male_youngAdult_ratingCount = ""
		# try:
		# 	male_elder_ratingCount = int(response.xpath('//div[@class="smallcell"]/a/text()').extract()[9].strip().replace(',',""))
		# except ValueError:
		# 	male_elder_ratingCount = ""
		
		try:
			female_teen_rating = float(response.xpath('//div[@class="bigcell"]/text()').extract()[11])
		except ValueError:
			female_teen_rating = ""
		try:
			female_youngAdult_rating = float(response.xpath('//div[@class="bigcell"]/text()').extract()[12])
		except ValueError:
			female_youngAdult_rating = ""
		try:
			female_adult_rating = float(response.xpath('//div[@class="bigcell"]/text()').extract()[13])
		except ValueError:
			female_adult_rating = ""
		try:
			female_elder_rating = float(response.xpath('//div[@class="bigcell"]/text()').extract()[14])
		except ValueError:
			female_elder_rating = ""
		try:
			female_ratingCount = int(response.xpath('//div[@class="smallcell"]/a/text()').extract()[10].strip().replace(',',""))
		except IndexError:
			female_ratingCount = ""

		# try:
		# 	female_teen_ratingCount = int(response.xpath('//div[@class="smallcell"]/a/text()').extract()[11].strip().replace(',',""))
		# except ValueError:
		# 	female_teen_ratingCount = ""
		# try:
		# 	female_youngAdult_ratingCount = int(response.xpath('//div[@class="smallcell"]/a/text()').extract()[12].strip().replace(',',""))
		# except ValueError:
		# 	female_youngAdult_ratingCount = ""
		# try:
		# 	female_adult_ratingCount = int(response.xpath('//div[@class="smallcell"]/a/text()').extract()[13].strip().replace(',',""))
		# except ValueError:
		# 	female_adult_ratingCount = ""
		# try:
		# 	female_elder_ratingCount = int(response.xpath('//div[@class="smallcell"]/a/text()').extract()[14].strip().replace(',',""))
		# except ValueError:
		# 	female_elder_ratingCount = ""

		try:
			us_users = float(response.xpath('//div[@class="bigcell"]/text()').extract()[17])
		except ValueError:
			us_users = ""
		# try:
		# 	us_count = int(response.xpath('//div[@class="smallcell"]/a/text()').extract()[17].strip().replace(',',""))
		# except ValueError:
		# 	us_count = ""
		try:
			non_USusers = float(response.xpath('//div[@class="bigcell"]/text()').extract()[18])
		except ValueError:
			non_USusers = ""
		# try:
		# 	non_UScount = int(response.xpath('//div[@class="smallcell"]/a/text()').extract()[18].strip().replace(',',""))
		# except ValueError:
		# 	non_UScount = ""

		item = ImdbItem()
		# item['run_time'] = run_time
		# item['genre'] = genre
		item['title'] = title
		# item['imdb_rating'] = imdb_rating
		# item['meta_rating'] = meta_rating
		item['MPAA_rating'] = MPAA_rating
		item['release_date'] = release_date
		item['director'] = director
		item['actors'] = actors
		item['male_teen_rating'] = male_teen_rating
		item['male_youngAdult_rating'] = male_youngAdult_rating
		item['male_adult_rating'] = male_adult_rating
		item['male_elder_rating'] = male_elder_rating
		item['male_ratingCount'] = male_ratingCount
		# item['male_teen_ratingCount'] = male_teen_ratingCount
		# item['male_youngAdult_ratingCount'] = male_youngAdult_ratingCount
		# item['male_adult_ratingCount'] = male_adult_ratingCount
		# item['male_elder_ratingCount'] = male_elder_ratingCount
		item['female_teen_rating'] = female_teen_rating
		item['female_youngAdult_rating'] = female_youngAdult_rating
		item['female_adult_rating'] = female_adult_rating
		item['female_elder_rating'] = female_elder_rating
		item['female_ratingCount'] = female_ratingCount
		# item['female_teen_ratingCount'] = female_teen_ratingCount
		# item['female_youngAdult_ratingCount'] = female_youngAdult_ratingCount
		# item['female_adult_ratingCount'] = female_adult_ratingCount
		# item['female_elder_ratingCount'] = female_elder_ratingCount
		item['non_USusers'] = non_USusers
		# item['non_UScount'] = non_UScount
		item['us_users'] = us_users
		# item['us_count'] = us_count


		yield item

