import scrapy
from urllib.parse import urljoin
from ..items import AmazonItem
from scrapy.loader import ItemLoader


class AmazonLaptopSpider(scrapy.Spider):
    name = 'amazon_laptop'
    # allowed_domains = ['https://www.amazon.fr/s?k=ordinateur+portable']
    start_urls = ['https://www.amazon.fr/s?k=ordinateur+portable/']

    

    
    def parse(self, response):
        links = response.css('a.a-link-normal.s-no-outline::attr(href)')
        for link in links:
            yield scrapy.Request(urljoin('https://www.amazon.fr', link.get()), callback=self.parse_link)


        #go to next page 
        next_page = response.css('ul.a-pagination li.a-last a::attr(href)')
        if  next_page is not None:
            yield scrapy.Request(next_page.get(), callback=self.parse)  

    
    def parse_link(self, response):
        # *******without using items.py *******
        
        # title = response.css('h1[id="title"] span[id="productTitle"]::text').get().strip()
        # review = response.css('div[id="averageCustomerReviews"] span.a-icon-alt::text').get().strip()
        # price =  response.css('div[id="price"] span.a-size-medium.a-color-price.priceBlockBuyingPriceString::text').get().strip()
        # yield{
        #     'title':title,
        #     'review':review,
        #     'price':price
        # }

        # ******using items.py file*********

        # item = AmazonItem()
        # item['title'] = response.css('h1[id="title"] span[id="productTitle"]::text').get().strip()
        # item['review'] = response.css('div[id="averageCustomerReviews"] span.a-icon-alt::text').get().strip()
        # item['price'] = response.css('div[id="price"] span.a-size-medium.a-color-price.priceBlockBuyingPriceString::text').get().strip()

        # yield item

        # using items & item loader 

        l = ItemLoader(item=AmazonItem(), selector=response)
        l.add_css('title', 'h1[id="title"] span[id="productTitle"]')
        l.add_css('review', 'div[id="averageCustomerReviews"] span.a-icon-alt')
        l.add_css('price', 'div[id="price"] span.a-size-medium.a-color-price.priceBlockBuyingPriceString')

        yield l.load_item()



        

