# <p align="center">Kayak: plan your trip</p>

![Kayak](https://seekvectorlogo.com/wp-content/uploads/2018/01/kayak-vector-logo.png)

## Context 

<a href="https://www.kayak.com" target="_blank">Kayak</a> is a travel search engine that helps user plan their next trip at the best price.

The marketing team needs help on a new project. After doing some user research, the team discovered that **70% of their users who are planning a trip would like to have more information about the destination they are going to**. 

In addition, user research shows that **people tend to be defiant about the information they are reading if they don't know the brand** which produced the content. 

Kayak Marketing Team would like to create an application that will recommend where people should plan their next holidays. The application should be based on real data about:

* Weather 
* Hotels in the area 

The application should then be able to recommend the best destinations and hotels based on the above variables at any given time. 

Marketing team wants to focus first on the top-35 cities to travel to in France, as chosen by <a href="https://one-week-in.com/35-cities-to-visit-in-france/" target="_blank">One Week In.com</a>

## Goal of the project
Obtain information on destinations from the top-35 cities list:
- GPS coordinates of the destination,
- Weather data for each destination,
- Hotel data for each destination.

The information should be combined in a single table containing enriched information about weather and hotels for each destination and stored in an S3 bucket. The same cleaned data should also be avalable as an SQL Database.

Based on this data, two maps should be delivered :
- Top-5 destinations,
- Top-20 hotels in these destinations.


## Project files
The different files of the project correspond to the steps that were accomplished to achieve the goal:

1. Gettiing gps coordinates of cities from list using API of https://nominatim.org/ 

        1_city_coordinates.ipynb
    
    The notebook creates the table city_coordinates.csv in the working directory and saves it to S3 bucket.

2. Getting weather forecast data for cities from list using API of https://openweathermap.org

        2_weather_data.ipynb

    The notebook creates the file weather_forecast.csv in the working directory and saves it to S3 bucket.


3. Scraping information on hotels from booking.com


Scraping Booking's search page to get hotel URLs and saving the resulting .json file to S3 bucket

        3a_booking_scraping_hotel_urls.py 
        3a_saving_hotel_urls_to_s3.ipynb


Scraping hotel pages to get hotel name, coordinates, score given by users, text description and saving the resulting .json file to S3 bucket.

        3b_booking_scraping_hotels_data.py
        3b_saving_hotels_data_to_s3.ipynb



4. Creating a unique table with enriched information for hotels in each city and saving it so S3 bucket

        4_kayak_df.ipynb

5. Creating an SQL Database using AWS RDS

        5_creating_sql_database_in_rds.ipynb

6. Creating maps with top-5 cities in terms of weather and top-20 hotels in each of these cities

        6_maps.ipynb

## Keys and credentials

API key for openweathermap.org as well as AWS credentials are confidential and are stored in an .env file as environment variables.

The files in S3 bucket are public for reading.


## References

- [Web Scraping Booking.Com](https://www.scrapingbee.com/blog/web-scraping-booking/) (Article with examples of code for scraping some types of data from booking.com pages)

- [Hide API keys in Python scripts using python-dotenv, .env, and .gitignore](https://www.youtube.com/watch?v=YdgIWTYQ69A/)

- [How to read a JSON response from a link in Python?](https://www.geeksforgeeks.org/how-to-read-a-json-response-from-a-link-in-python/)

- [Connecting to a relational database using SQLAlchemy and Python](https://dev.to/chrisgreening/connecting-to-a-relational-database-using-sqlalchemy-and-python-1619/)