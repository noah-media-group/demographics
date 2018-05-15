from scrapy import Spider, Request
from imdb_pt1.items import ImdbPt1Item
import re

class imdb1Spider(Spider):
	name = 'imdb1_spider'
	allowed_urls = ['https://www.imdb.com/']
	start_urls = ['https://www.imdb.com/search/title?title_type=feature&release_date=2000-01-01,2018-05-31&num_votes=10000,&countries=us&page=1&ref_=adv_nxt']

	def parse(self, response):
		
		#find total number of pages and movies
		regex = '[(\d+,)]*\d+'
		tot_titles = int((re.findall(regex,response.xpath('//div[@class="desc"]/text()').extract()[2])[0]).replace(',',""))
		pg1 = int(response.xpath('//span[@class="lister-current-first-item"]/text()').extract_first())
		per_page = int(response.xpath('//span[@class="lister-current-last-item"]/text()').extract_first())

		number_pages = tot_titles//per_page + 1

		request_url = ['https://www.imdb.com/search/title?title_type=feature&release_date=2000-01-01,2018-05-31&num_votes=10000,&countries=us&page={}&ref_=adv_nxt'.format(x) for x in range(1,number_pages)]


		for url in request_url:
			yield Request(url=url, callback=self.parse_resultPage)

	def parse_resultPage(self, response):

		#scraping details on movie results page
		movie_list = response.xpath('//div[@class ="lister-item-content"]')

		for details in movie_list:
			title = details.xpath('.//h3[@class="lister-item-header"]/a/text()').extract_first()
			run_time = int(re.findall('\d+',details.xpath('.//span[@class="runtime"]/text()').extract_first())[0])
			genre = details.xpath('.//span[@class="genre"]/text()').extract_first().strip()
			try:
				gross = float(details.xpath('.//span[@name="nv"]/text()').extract()[1].replace('$',"").replace('M',""))
			except IndexError:
				gross = ""
			imdb_rating = float(details.xpath('.//div[@class="inline-block ratings-imdb-rating"]/strong/text()').extract_first())
			try:
				meta_rating = int(details.xpath('.//div[@class="inline-block ratings-metascore"]/span/text()').extract_first())
			except TypeError:
				meta_rating = ""

			item = ImdbPt1Item()
			item['run_time'] = run_time
			item['genre'] = genre
			item['title'] = title
			item['imdb_rating'] = imdb_rating
			item['meta_rating'] = meta_rating
			item['gross'] = gross

			yield item