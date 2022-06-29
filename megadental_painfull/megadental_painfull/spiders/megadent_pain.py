import scrapy
import re
import ast

class MegadentPainSpider(scrapy.Spider):
    name = 'megadent_pain'


    # with open("skipped_product.txt",'r') as ip_file:
    #     skipped_products = ip_file.readlines()
    # skipped_products_clean_urls = []
    # for item in skipped_products:
    #     item = item.split('\n')
    #     skipped_products_clean_urls.append(item[0])


    def start_requests(self):

        skipped_products_clean_urls = []

        with open("painfull_product.txt",'r') as ip_file:
            skipped_products = ip_file.readlines()
        

        for item in skipped_products:
            item = item.split('\n')
            skipped_products_clean_urls.append(item[0])

        print(len(skipped_products_clean_urls))

        # skipped_products_clean_urls = ['https://www.megadental.fr/3m-bloc-melange-empreintes-boite-de-10.html']

        for url in skipped_products_clean_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            

     
    
    
    def parse(self, response):

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


        configs = response.css('div.product-options-wrapper div.fieldset div.field.configurable.required')


        if int(len(configs)) == 1:
            # url = response.request.url
            designation = product_detail.css('div.page-title-wrapper.product h1.page-title span[data-dynamic="product_name"]::text').get().strip()
            reference = product_detail.css('div.product.attibute.code_mega.sku div.value[itemprop="sku"]::text').get()
            marque = product_detail.css('span.product-brand a::attr(href)').get()
            if marque is not None :
               marque =  marque.split('/')[-1]
            else:
                marque = ''

            descriptif = ''.join(product_detail.css('div.product.data.contenu div.product.attribute.description p::text').getall()).replace(',',' ')
            id_variante =  product_detail.css('div::attr(data-product-id)').get()

          
            

            script = response.css('div.product-options-wrapper script').get()

            option_names = re.findall(r'code\":\"(.+?)\",\"label\"',script)

            option_values = re.findall(r',\"options\":\[(.+?)],',script)

            option_prices = re.findall(r'\"optionPrices\":(.+?),\"priceFormat\":',script)

            option_name_values = {}
            j = 1  


            # extract confgi permutations & combinations
            while(j <= len(option_names)):
                for item in option_values:
                    # print(item)
                    dict_temp = {}
                    new_item = ast.literal_eval(item)
                    if type(new_item) == tuple:
                        for i in new_item:
                            # print(i)
                            # print(f"{i['label']}:{i['products']}")
                            dict_temp.update({i['label'] : i['products']})
                            
                    if type(new_item) == dict:
                        # print(type(new_item))
                        # print(f"{item['label']}:{item['products']}")
                        dict_temp.update({new_item['label'] : new_item['products']})
                    
                    option_name_values[option_names[j-1]] = dict_temp   
                    j+= 1

            # print(option_name_values)   

            option_name_values['option_prices'] = option_prices
            product_options = option_name_values
            

            attribute = list(product_options.keys())[0]
            att_value = list(product_options[attribute].keys())


            prod_price = ast.literal_eval(product_options['option_prices'][0])

            for prod_label in att_value:

                prod_id = ''.join(product_options[attribute][prod_label])

                old_Price = prod_price[prod_id]['oldPrice']['amount']
                base_price = prod_price[prod_id]['basePrice']['amount']
                besttier_Price = prod_price[prod_id]['besttierPrice']['amount']
                final_price = prod_price[prod_id]['finalPrice']['amount']
                tier_price = prod_price[prod_id]['tierPrices']


                if int(len(tier_price)) == 1:
                    qty_dgrsf_1 = tier_price[0]['qty']
                    qty_dgrsf_2 = ''
                    prix_prom_dgrsf_1 = tier_price[0]['price']
                    prix_prom_dgrsf_2 = ''

                if int(len(tier_price)) == 2:
                    qty_dgrsf_1 = tier_price[0]['qty']
                    qty_dgrsf_2 = tier_price[1]['qty']
                    prix_prom_dgrsf_1 = tier_price[0]['price']
                    prix_prom_dgrsf_2 = tier_price[1]['price']   

                yield{

                    'url': response.request.url,
                    'marque' : marque,
                    'id_variante' : id_variante,
                    'designation' : designation,
                    'reference' : reference ,
                    'descriptif': descriptif,
                    'atribute':attribute,
                    'attribute_value': prod_label,
                    'prix_promo_unit': besttier_Price,
                    'ref_price_unit': old_Price,
                    'qty_dgrsf_1' : qty_dgrsf_1,
                    'qty_dgrsf_2' : qty_dgrsf_2,
                    'prix_prom_dgrsf_1' : prix_prom_dgrsf_1,
                    'prix_prom_dgrsf_2' : prix_prom_dgrsf_2

                    }                
    

                    


                

        else: 
            with open("more_than_1_option.txt",'a') as painfull_product_url:
                painfull_product_url.write(f"{response.request.url}\n")

            painfull_product_url.close()    

                                

                
            



            