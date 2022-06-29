import scrapy


class DinasoursSpider(scrapy.Spider):
    name = 'dinasours'
    # allowed_domains = ['example.com']
    start_urls = ['https://www.thoughtco.com/dinosaurs-a-to-z-1093748']

    def parse(self, response):
        for link in response.css('p[id^=mntl-sc-block_] a::attr(href)').getall():
            if 'https://www.thoughtco.com/' in link :
                yield scrapy.Request(link, callback=self.parse_dino)
        

    def parse_dino(self, response):
    
        for dino in response.css('div[id^=list-sc-item]'):
            image_url = dino.css('div.img-placeholder img::attr(data-src)').get()
            all_details = dino.css('p::text').getall()
            
            try: 
                yield {
                    'name' : all_details[1].strip(), 
                    'habitat' : all_details[3].strip(),
                    'historical_period': all_details[5].strip(),
                    'size_weight': all_details[7].strip(),
                    'characterstics'  :all_details[9].strip(),
                    'image_url' : image_url
            }
            except IndexError:
                pass

           