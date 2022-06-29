# TODO : next page 
# url refre before assgnmt 

import scrapy
import re


class SpidermegadentalSpider(scrapy.Spider):
    name = 'SpiderMegadental'
    # allowed_domains = ['megadental.fr']
    # start_urls = ['http://megadental.fr/']

    def start_requests(self):
        urls = [
            'http://megadental.fr/',
        ]
        for url in urls:
                        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for link in response.css('div.page-wrapper div.sections.nav-sections div.section-item-content.nav-sections-item-content nav.navigation li div.row div.nav-item a::attr(href)'):
           yield response.follow(link.get(), callback=self.parse_link)


        next_page =  response.css('li.item.pages-item-next a::attr(href)').get()
        
        if  next_page is not None:
            yield scrapy.Request(next_page.get(), callback=self.parse) 


    def parse_link(self, response):
        for product_link in response.css('div.page-wrapper main[id="maincontent"] div.column.main div.products.wrapper.grid.products-grid li.item.product.product-item div.product-item-info a.product.photo.product-item-photo.product-item-link::attr(href)'):
            yield response.follow(product_link.get(), callback=self.parse_product)

    
    
    
    def parse_product(self, response):

        product_detail = response.css('div.columns')

        url = None
        marque  = None
        id_variante = None
        designation = None
        reference = None
        descriptif= None
        besttier_Price= None
        final_price= None
        qty_dgrsf_1 = None
        qty_dgrsf_2 = None
        prix_prom_dgrsf_1 = None
        prix_prom_dgrsf_2 = None
        base_price = None
        old_Price = None
        painfull_product_url = None


        if response.css('div.product-options-wrapper script').get() == None:
            # url = response.request.url
            designation = product_detail.css('div.page-title-wrapper.product h1.page-title span[data-dynamic="product_name"]::text').get().strip()
            reference = product_detail.css('div.product.attibute.code_mega.sku div.value[itemprop="sku"]::text').get().strip()
            marque = product_detail.css('span.product-brand a::attr(href)').get()
            if marque is not None :
               marque =  marque.split('/')[-1]
            else:
                marque = ''

            descriptif = ''.join(product_detail.css('div.product.data.contenu div.product.attribute.description p::text').getall()).replace(',',' ')
            id_variante =  product_detail.css('div::attr(data-product-id)').get()
            
            response_string = response.text
            base_price = re.findall(r'basePrice\":{\"amount\":(.+?),"', response_string)
            final_price = re.findall(r'finalPrice\":{\"amount\":(.+?),"', response_string)
            besttier_Price = re.findall(r'besttierPrice\":{\"amount\":(.+?),"', response_string) #promotional price
            old_Price = re.findall(r'oldPrice\":{\"amount\":(.+?),"', response_string) # refrence 

            degresif_dict = {}

            if len(response.css('div.product-info-price-sku ul.prices-tier.items li').getall()) > 0 :
                for i in range(0, len(response.css('div.product-info-price-sku ul.prices-tier.items li'))):
                    quantity = response.css('div.product-info-price-sku ul.prices-tier.items li.item::text').getall()[i].split()[1]
                    price = response.css('div.product-info-price-sku ul.prices-tier.items li.item span.price-container span::attr(data-price-amount)').getall()[i].strip()
                    degresif_dict[quantity] = price

                if len(list(degresif_dict.keys())) == 2 :
                    qty_dgrsf_1 = list(degresif_dict.keys())[0]
                    qty_dgrsf_2 = list(degresif_dict.keys())[1]
                    prix_prom_dgrsf_1 = list(degresif_dict.values())[0]
                    prix_prom_dgrsf_2 = list(degresif_dict.values())[1] 

                if len(list(degresif_dict.keys())) == 1 :
                    qty_dgrsf_1 = list(degresif_dict.keys())[0]
                    qty_dgrsf_2 = list(degresif_dict.keys())[1]
                    prix_prom_dgrsf_1 =''
                    prix_prom_dgrsf_2 = ''  
            else:
                qty_dgrsf_1 = ''
                qty_dgrsf_2 = ''
                prix_prom_dgrsf_1 =''
                prix_prom_dgrsf_2 = ''

        else: 
            with open("painfull_product.txt",'a') as painfull_product_url:
                painfull_product_url.write(f"{response.request.url}\n")

            painfull_product_url.close()    

                            

            
        



        yield{

        'url': response.request.url,
        'marque' : marque,
        'id_variante' : id_variante,
        'designation' : designation,
        'reference' : reference ,
        'descriptif': descriptif,
        'prix_promo_unit': besttier_Price,
        'ref_price_unit': old_Price,
        'qty_dgrsf_1' : qty_dgrsf_1,
        'qty_dgrsf_2' : qty_dgrsf_2,
        'prix_prom_dgrsf_1' : prix_prom_dgrsf_1,
        'prix_prom_dgrsf_2' : prix_prom_dgrsf_2

        }                


         
           

