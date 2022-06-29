import scrapy
import requests
import ast


class HenryscheinspiderSpider(scrapy.Spider):
    name = 'henryscheinspider'
    # allowed_domains = ['www.henryschein.fr/fr-fr/shopping/SupplyBrowser.aspx']
    start_urls = ['https://www.henryschein.fr/fr-fr/shopping/SupplyBrowser.aspx']
    # start_urls = ['https://www.henryschein.fr/fr-fr/dental/p/anesthesie-pharmacie/aiguilles/aiguilles-anesthesie-intraligamentaires-cybertech-30g-s-0-30x13mm-boite-de-100/900-6527']
    

    

    def parse(self, response):        
        yield response.follow('https://www.henryschein.fr/fr-fr/shopping/SupplyBrowser.aspx', callback=self.parse_redirect)
        
        
    
    def parse_redirect(self, response):
        category_url = response.css('ul.hs-categories.display.grid.clear-fix li.item a::attr(href)')
        # print("All urls ", category_url)
        for url in category_url:
           yield response.follow(url.get(), callback=self.parse_sub_category)
           

    def parse_sub_category(self, response):
        sub_category_url = response.css('ul.hs-categories.display.grid.clear-fix li.item a::attr(href)')
        for url in sub_category_url:
            yield response.follow(url.get(), callback=self.parse_product_link)


    def parse_product_link(self, response):
        product_url = response.css('ol.products.most-relevant.simple.hs-form li div.title.first h2.product-name a::attr(href)')
        for url in product_url:
            yield response.follow(url.get(), callback=self.parse_product_details)

        try:
            total_pages = int(response.css('div.half div.hs-paging.no-border-bottom.float-arrows::attr(data-total)').get())
        except:
            total_pages = 0    

        base_url = response.url

        url_slice = base_url.split('?')

        if len(url_slice) > 1 : 
            base_url = url_slice[0]
        else:
            base_url = base_url

        if total_pages > 1 : 
            for i in range(2, total_pages + 1):
                yield response.follow(f"{base_url}?pagenumber={i}", callback=self.parse_product_link)
                    



    def parse_product_details(self, response):

        script = response.css('main.container script[type="application/ld+json"]').get()
        script = ast.literal_eval(script[35:-9])
        product_details = response.css('ul.product-summary li')

        try:

            url = script['url']
            marque = script['brand']['name'] 
            id_variante = script['sku'] 
            designation = script['name']
            description = script['description'] 
            code_article =   script['mpn']
            reference = script['sku']
            sku = script['sku']
            prix_promo_unit = script['offers']['price']
            prix_ref_unit = product_details.css('div.value.clear-fix ul.product-actions span.price-mod.hs-strike.color-gray.x-small::text').get()
            prom_qty = product_details.css('div.value.clear-fix ul.product-actions span.medium.custom-style-quantity::text').get()[-1]
            prom_prc = product_details.css('div.value.clear-fix ul.product-actions span.x-large.color-quaternary.custom-style-price::text').get().split(' ') [0].replace(',','')

        except:
            url = script['url']
            marque = script['brand']['name'] 
            id_variante = script['sku'] 
            designation = script['name']
            description = script['description'] 
            code_article =   script['mpn']
            reference = script['sku']
            sku = script['sku']
            prix_promo_unit = script['offers']['price']
            prix_ref_unit = ' '
            prom_qty = ' '
            prom_prc = ' '


        if prix_ref_unit == ' ':
            prix_ref_unit = prix_promo_unit
            prix_promo_unit = ' '

        yield{

           'url': url,
           'marque':marque,
           'id_variante' : id_variante,
           'designation' : designation,
           'descriptif' : description,
           'code_article' : code_article,
           'reference' : reference,
           'sku':sku,
           'prix_promo_unit':prix_promo_unit,
           'prix_ref_unit':prix_ref_unit,
           'prom_qty':prom_qty,
           'prom_prc':prom_prc
           
        }    
            
            


