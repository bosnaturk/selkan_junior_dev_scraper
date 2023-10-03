import scrapy
import re

class Car24ComSpider(scrapy.Spider):
    name = 'mycrawler'
    allowed_domains = ['cars24.com']
    start_urls = ['https://www.cars24.com/ae/buy-used-cars-dubai/']

    def parse(self, response):
        # Print the URL of the current page
        print("URL:", response.url)
        
        # Loop through each car ad on the page
        for ad in response.css('._3IIl_._1xLfH'):
            # Extract the brand and other data
            brand = ad.css('._3TSwN>.RZ4T7::text').get()
            engine_size = ad.css("ul._3ZoHn>li::text")[2].get()
            
            # Extract the text from the p element and use a regular expression to get the year
            year_text = ad.css('._1i1E6::text').get()
            year = re.search(r'\b\d{4}\b', year_text).group() if year_text else None
            
            deeplink = ad.css('._1Lu5u::attr(href)').get()
            price = ad.css('._7yds2::text').get()
            mileage = ad.css("ul._3ZoHn>li::text")[1].get()

            # Create a new dictionary for the scraped data
            car_data = {
                'Brand': brand,
                'Engine Size': engine_size,
                'Year of Manufacture': year,
                'Deeplink': response.urljoin(deeplink),
                'Price': price,
                'Mileage': mileage,
            }

            # Pass the car_data dictionary to the parse_details method
            yield scrapy.Request(url=response.urljoin(deeplink), callback=self.parse_details, meta=car_data)

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

