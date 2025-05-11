import os
import json
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

# 👉 L'utilisateur entre les infos AVANT le lancement du spider
restaurant_type = input("Quel type de restaurant ? ").replace(" ", "+")
location = input("Dans quelle ville ? ").replace(" ", "+")

class YelpSpider(scrapy.Spider):
    name = 'yelp'

    def __init__(self, restaurant_type, location, **kwargs):
        super().__init__(**kwargs)
        self.restaurant_type = restaurant_type
        self.location = location
        self.start_urls = [
            f'https://www.yelp.fr/search?find_desc={self.restaurant_type}&find_loc={self.location}',
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

# nom dynamique du fichier
filename = f"restaurant_{restaurant_type}-{location}.json"

if filename in os.listdir('results/'):
    os.remove('results/' + filename)

process = CrawlerProcess(settings={
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'results/' + filename: {"format": "json"},
    }
})

# 👉 les paramètres sont passés ici au spider
process.crawl(YelpSpider, restaurant_type=restaurant_type, location=location)
process.start()
