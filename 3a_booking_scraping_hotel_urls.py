import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess



city_list = ["Mont Saint Michel", 
                        "St Malo",
                        "Bayeux",
                        "Le Havre",
                        "Rouen",
                        "Paris",
                        "Amiens",
                        "Lille",
                        "Strasbourg",
                        "Chateau du Haut Koenigsbourg",
                        "Colmar",
                        "Eguisheim",
                        "Besancon",
                        "Dijon",
                        "Annecy",
                        "Grenoble",
                        "Lyon",
                        "Gorges du Verdon",
                        "Bormes les Mimosas",
                        "Cassis",
                        "Marseille",
                        "Aix en Provence",
                        "Avignon",
                        "Uzes",
                        "Nimes",
                        "Aigues Mortes",
                        "Saintes Maries de la mer",
                        "Collioure",
                        "Carcassonne",
                        "Ariege",
                        "Toulouse",
                        "Montauban",
                        "Biarritz",
                        "Bayonne",
                        "La Rochelle"]

city_list.sort()

print(city_list)

adapted_city_list = []
for i in range(0, len(city_list)):
    new_city_name = city_list[i].replace(" ", "+")
    adapted_city_list.append(new_city_name)

print(adapted_city_list)

url_list = []
for i in range(0, len(adapted_city_list)):
    url = "https://www.booking.com/searchresults.en-us.html?ss=city&ssne=city&ssne_untouched=city&order=distance_from_search"
    # &order=distance_from_search: the hotels in the search results will be sorted by distance from the city center
    # (closest hotels first)
    new_url = url.replace("city", adapted_city_list[i])
    url_list.append(new_url)

print(url_list)

print(len(url_list))
                
class booking_spider(scrapy.Spider):
    # Naming the spider
    name = "booking"


    # Urls for the spider to start from 
    start_urls = url_list

    # Callback function that will be called when starting your spider
    # It will get text, author and tags of the first <div> with class="quote"
    def parse(self, response):
        property_cards = response.xpath('.//div[@data-testid="property-card"]')
        for property_card in property_cards: 
            url = property_card.xpath('.//h3/a[@data-testid="title-link"]/@href').get().split("?")[0]
            url_dict = {
                #"hotel_name": response.xpath('.//h3/a[@data-testid="title-link"]/div/text()').get(),
                "hotel_name": property_card.xpath('.//h3/a[@data-testid="title-link"]/div/text()').get(),
                "hotel_url" : url,
                "booking_city_url": response
                #"city": city
                #"score": response.xpath('.//div[@data-testid="review-score"]/div/text()').get(""),
                #"location": response.xpath('.//span[@data-testid="address"]/text()').get("")
                    }
            try:
                yield url_dict
            except:
                    return None

filename = "booking_search_page.json"


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