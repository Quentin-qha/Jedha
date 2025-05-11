import os
import json
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

class YelpSpider(scrapy.Spider):
    name = 'yelp'

    restaurant_type = 'restaurant+japonais'
    location = 'paris'

    start_urls = [
        f'https://www.yelp.fr/search?find_desc={restaurant_type}&find_loc={location}',
    ]

    def parse(self, response):
        for restaurant in response.css('.y-css-pwt8yl'):
            yield {
                'name': restaurant.css('.y-css-1x1e1r2::text').get(),
                'location': restaurant.css('.y-css-yvhxeq::text').get(),
                'rating': restaurant.css('.y-css-f73en8::text').get(),
                'nb_reviews': restaurant.css('.y-css-1vi7y4e::text').get(),
                'url': restaurant.css('.y-css-1x1e1r2').attrib["href"],
            }

            next_page = response.css('a.next-link::attr(href)').get()
            if next_page:
                yield response.follow(next_page, self.parse)
            else:
                self.logger.info("Dernière page atteinte.")




filename = "restaurant_japonais-paris.json"

if filename in os.listdir('results/'):
        os.remove('results/' + filename)

process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'results/' + filename : {"format": "json"},
    }
})

process.crawl(YelpSpider)
process.start()