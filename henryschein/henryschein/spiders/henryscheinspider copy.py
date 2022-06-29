import scrapy
import requests


class HenryscheinspiderSpider(scrapy.Spider):
    name = 'dummy'
    # allowed_domains = ['www.henryschein.fr/fr-fr/shopping/SupplyBrowser.aspx']
    start_urls = ['https://www.henryschein.fr/fr-fr/shopping/SupplyBrowser.aspx']
    

    

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

        total_pages = int(response.css('div.half div.hs-paging.no-border-bottom.float-arrows::attr(data-total)').get())

        base_url = response.url

        if total_pages > 1 : 
            for i in range(2, total_pages+1):
                yield response.follow(f"{base_url}?pagenumber={i}", callback=self.parse_product_link)
                    



    def parse_product_details(self, response):

        product_details = response.css('ul.product-summary li')

        url = response.url
        designation = product_details.css('h2.product-title.medium.strong::text').get().strip()
        ref = product_details.css('h2.product-title.medium.strong small.x-small strong::text').get().strip()
        id = product_details.css('h2.product-title.medium.strong small.x-small::text').getall()[0].split()[-1]
        Marque = product_details.css('h2.product-title.medium.strong small.x-small::text').getall()[0].split('-')[0].split('|')[1].strip()
        description = product_details.css('li.customer-notes div.value::text').get().strip()
        old_price = product_details.css('div.value.clear-fix ul.product-actions span.price-mod.hs-strike.color-gray.x-small::text').get()
        new_price = product_details.css('div.value.clear-fix ul.product-actions span.amount.x-small::text').get()
        prom_qty = product_details.css('div.value.clear-fix ul.product-actions span.medium.custom-style-quantity::text').get()
        prom_prc = product_details.css('div.value.clear-fix ul.product-actions span.x-large.color-quaternary.custom-style-price::text').get()



        yield{

            'URL':  url,
            'DESIGNATION':designation,
            'REFERENCE' : ref,
            'ID_VARIANTE': id,
            'MARQUE': Marque,
            'DESCRIPTIF':description,
            'PRIX_DE_REFERENCE_UNITAIRE': old_price,
            'PRIX_PROMOTIONNEL_UNITAIRE': new_price,
            'QUANTITE DEGRESSIF 1':prom_qty,
            'PRIX_PROMOTIONNEL_DEGRESSIF_1':prom_prc,

        }    
            
            


