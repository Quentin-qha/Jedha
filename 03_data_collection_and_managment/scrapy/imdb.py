import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

class imdb_spider(scrapy.Spider):
    name = "imdb"

    start_urls = [
        'https://www.imdb.com/chart/boxoffice',
    ]

    def parse(self, response):
        for movie in response.css('.ipc-metadata-list-summary-item'):
            yield {
                "title": movie.css('.ipc-title__text::text').get(),
                "url": movie.css('.ipc-title-link-wrapper').attrib["href"],
                "total_earnings": movie.xpath('.//li[span[contains(text(), "Total Gross")]]/span[2]/text()').get(),
                "rating": movie.css('.ipc-rating-star--rating::text').get(),
                "nb_voters": movie.css('.ipc-rating-star--voteCount::text').getall() 
            }

filename = "imdb1.json"

if filename in os.listdir('01-Become_a_movie_director/'):
        os.remove('01-Become_a_movie_director/' + filename)

process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        '01-Become_a_movie_director/' + filename : {"format": "json"},
    }
})

process.crawl(imdb_spider)
process.start()