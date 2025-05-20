import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from cities import cities

city_to_url = {
    city: f"https://www.booking.com/searchresults.fr.html?ss={city.replace(' ', '+')}&lang=fr&ac_suggestion_list_length=20&search_selected=true&group_adults=2&group_children=0"
    for city in cities
}

#changer le .env pour le mettre à la racine de l'ordi
class hotelSpider(scrapy.Spider):
    name = "hotel_spider"

    def start_requests(self):
        for index, city in enumerate(cities):
            city_url = city.replace(" ", "+")
            url = f"https://www.booking.com/searchresults.fr.html?ss={city_url}&lang=fr"
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={"city": city, "city_index": index}
            )

    def parse(self, response):
        city = response.meta["city"]
        city_index = response.meta["city_index"]

        for hotel in response.css('[role="listitem"]'):
            name = hotel.css('h3 [data-testid="title"]::text').get()
            link = hotel.css('h3 [data-testid="title-link"]::attr(href)').get()

            stars = len(hotel.css('[data-testid="rating-stars"] span').getall())
            rating = hotel.css('[data-testid="review-score"] .f63b14ab7a::text').get()
            description = hotel.css('div.fff1944c52::text').get()

            yield response.follow(
                url=link,
                callback=self.parse_hotel,
                meta={
                    "city_id": city_index,
                    "city": city,
                    "name": name,
                    "stars": stars,
                    "rating": rating,
                    "description": description
                }
            )

    def parse_hotel(self, response):
        coords = response.css('[data-atlas-latlng]::attr(data-atlas-latlng)').get()
        if coords:
            lat, lon = coords.strip().split(',')
        else:
            lat, lon = '', ''

        yield {
            "city_id": response.meta["city_id"],
            "city": response.meta["city"],
            "name": response.meta["name"],
            "link": response.url,
            "latitude": lat,
            "longitude": lon,
            "description": response.meta["description"],
            "stars": response.meta["stars"],
            "rating": response.meta["rating"]
        }

filename = "hotels.json"
from pathlib import Path


if filename in os.listdir('export/'):
        os.remove('export/' + filename)

process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'export/' + filename : {"format": "json"},
    }
})

process.crawl(hotelSpider)
process.start()