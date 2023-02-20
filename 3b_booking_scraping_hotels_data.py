import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

import json
from urllib.request import urlopen

#with open('C:\\Study\\Jedha\\Fullstack\\dmc_19_10_2022\\kayak_project\\result\\booking24_search_page.json') as hotels:
   #hotels = json.load(hotels)

url = "https://kayak-booking-bucket-12-12-2022.s3.eu-west-3.amazonaws.com/booking_search_page.json"

response = urlopen(url)
hotels = json.loads(response.read())

# Creating a list of hotel urls to indicate pages to be scraped
hotel_url_list = []
for i in range(0, len(hotels)):
    hotel_url_list.append(hotels[i]["hotel_url"])

class booking_spider(scrapy.Spider):
    # Naming the spider
    name = "booking"

    # Urls for the spider to start from:
    start_urls = hotel_url_list

    # Callback function that will be called when starting the spider
    def parse(self, response):
        return {
                "hotel_name": response.xpath('.//*[@class="d2fee87262 pp-header__title"]/text()').get(),
                "score": response.xpath('.//*[@class="b5cd09854e d10a6220b4"]/text()').get(),
                "description": ' '.join((response.xpath('.//*[@id="property_description_content"]/p/text()').getall())),
                "location": response.xpath('.//*[@id="showMap2"]/span[1]/text()').get(""),
                # Description of a hotel is separated in several phrases, each of phrases enclosed in a tag <p></p>
                # I'm using the 'join()' method to join the different phrases of the description into a single string.
                "latitide": (response.xpath('.//*[@id="hotel_sidebar_static_map"]/@data-atlas-latlng').get()).split(',')[0],
                "longtitude": (response.xpath('.//*[@id="hotel_sidebar_static_map"]/@data-atlas-latlng').get()).split(',')[1],
                "hotel_url": response
                # Extracting the value of latitude and longtitude from the same attribute whose value had the form of a tuple (latitude, longtitude)
                # using indexes, the of latitude and longtitude are extracted and saved as separate dictionary items.
                    }

filename = "booking_hotels_data.json"

# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
if filename in os.listdir('result/'): 
        os.remove('result/' + filename)

# Declaring a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'result/' + filename : {"format": "json"},
    }
})

# Starting the crawling using the spider defined above
process.crawl(booking_spider)
process.start()