import scrapy
import re

class Car24ComSpider(scrapy.Spider):
    name = 'mycrawler'
    allowed_domains = ['cars24.com']
    start_urls = ['https://www.cars24.com/ae/buy-used-cars-dubai/']
    base_xhr_url = 'https://listing-service.c24.tech/v2/vehicle?sf=city:DU&sf=gaId:&size=25&spath=buy-used-cars-dubai&page={}&variant=filterV5'
    page_number = 1  # Start with page 1

    def parse(self, response):        
        # Loop through each car ad on the page
        for ad in response.css('._3IIl_._1xLfH'):
            # ... [Your scraping logic remains unchanged] ...

            # Pass the car_data dictionary to the parse_details method
            yield scrapy.Request(url=response.urljoin(deeplink), callback=self.parse_details, meta=car_data)

        # Pagination: Increment the page number and send a request to the next page's URL
        self.page_number += 1
        next_page_url = self.base_xhr_url.format(self.page_number)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        # Retrieve the data passed from the previous method
        item = {
            'Brand': response.meta['Brand'],
            'Engine Size': response.meta['Engine Size'],
            'Year of Manufacture': response.meta['Year of Manufacture'],
            'Deeplink': response.meta['Deeplink'],
            'Price': response.meta['Price'],
            'Mileage': response.meta['Mileage'],
        }
        
        # Extract the Fuel Type from the details page
        fuel_type = response.css('._1xlKo>.v2mgh::text')[5].get()
        
        # Add the Fuel Type to the item and yield it
        item['Fuel Type'] = fuel_type
        yield item