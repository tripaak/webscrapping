import scrapy
import re
import ast
import itertools
from scrapy.crawler import CrawlerProcess

class Megadental2Spider(scrapy.Spider):
    
    name = 'megadental_2'
    
    
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


        configs = response.css('div.product-options-wrapper div.fieldset div.field.configurable.required')

        print(len(configs))
        
        product_detail = response.css('div.columns')

        if response.css('div.product-options-wrapper script').get() == None:
            
            try:
                product_add_cart_form = response.css('div.product-add-form.configurable div.fieldset script[type="text/x-magento-init"]').getall()[0].strip()
            except:
                pass
            product_detail = response.css('div.columns')

            reference = product_detail.css('div.product.attibute.code_mega.sku div.value[itemprop="sku"]::text').get()
            
            if reference is not None:
                reference = reference.strip()
                
            else:    
                reference = re.findall(r'Code article fournisseur :(.+?)<', product_add_cart_form)
                if len(reference) > 0:
                    reference = reference[0]
                else:    
                    reference = re.findall(r'\"code_mega\":\{\"(\d*)\":{\"id\":\"(\d*-\d*)\",\"value\":\"(\d*-\d*)\"},', product_add_cart_form)
                    if len(reference) > 0:
                        reference= reference[0][-1]
                    else:
                        reference = 'Not Found'
            
            
            marque = product_detail.css('span.product-brand a::attr(href)').get()

            if marque is not None :
                marque =  marque.split('/')[-1]
            else:
                marque = re.findall(r'\"marque\":{\"(.+?)\":{\"id\":\"(.+?)\",\"value\":\"(.+?)\"},', product_add_cart_form)
                
                if len(marque) > 0:
                    marque= marque[0][-1]
                else:
                    marque = 'Not Found'


            designation = product_detail.css('div.page-title-wrapper.product h1.page-title span[data-dynamic="product_name"]::text').get().strip()
            # reference = product_detail.css('div.product.attibute.code_mega.sku div.value[itemprop="sku"]::text').get().strip()
            # marque = product_detail.css('span.product-brand a::attr(href)').get()
            # if marque is not None :
            #    marque =  marque.split('/')[-1]
            # else:
            #     marque = ''

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

            yield{
                'url': response.request.url,
                'marque' : marque,
                'id_variante' : id_variante,
                'designation' : designation,
                'reference' : reference ,
                'descriptif': descriptif,
                'atribute1':' ',
                'attribute_1_value': ' ',
                'atribute2':' ',
                'attribute_2_value': ' ',
                'atribute3': ' ',
                'attribute_3_value': ' ',
                'prix_promo_unit': besttier_Price,
                'ref_price_unit': old_Price,
                'qty_dgrsf_1' : qty_dgrsf_1,
                'qty_dgrsf_2' : qty_dgrsf_2,
                'prix_prom_dgrsf_1' : prix_prom_dgrsf_1,
                'prix_prom_dgrsf_2' : prix_prom_dgrsf_2
            }    

            

        if int(len(configs)) == 1:
            # url = response.request.url
            designation = product_detail.css('div.page-title-wrapper.product h1.page-title span[data-dynamic="product_name"]::text').get().strip()
            # reference = product_detail.css('div.product.attibute.code_mega.sku div.value[itemprop="sku"]::text').get()
            # marque = product_detail.css('span.product-brand a::attr(href)').get()
            
            try:
                product_add_cart_form = response.css('div.product-add-form.configurable div.fieldset script[type="text/x-magento-init"]').getall()[0].strip()
            except:
                pass
            
            product_detail = response.css('div.columns')

            reference = product_detail.css('div.product.attibute.code_mega.sku div.value[itemprop="sku"]::text').get()
            
            if reference is not None:
                reference = reference.strip()
                
            else:    
                reference = re.findall(r'Code article fournisseur :(.+?)<', product_add_cart_form)
                if len(reference) > 0:
                    reference = reference[0]
                else:    
                    reference = re.findall(r'\"code_mega\":\{\"(\d*)\":{\"id\":\"(\d*-\d*)\",\"value\":\"(\d*-\d*)\"},', product_add_cart_form)
                    if len(reference) > 0:
                        reference= reference[0][-1]
                    else:
                        reference = 'Not Found'
            
            
            marque = product_detail.css('span.product-brand a::attr(href)').get()

            if marque is not None :
                marque =  marque.split('/')[-1]
            else:
                marque = re.findall(r'\"marque\":{\"(.+?)\":{\"id\":\"(.+?)\",\"value\":\"(.+?)\"},', product_add_cart_form)
                
                if len(marque) > 0:
                    marque= marque[0][-1]
                else:
                    marque = 'Not Found'


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
                    'atribute1':' ',
                    'attribute_1_value': ' ',
                    'atribute2':' ',
                    'attribute_2_value': ' ',
                    'atribute3': ' ',
                    'attribute_3_value': ' ',
                    'prix_promo_unit': besttier_Price,
                    'ref_price_unit': old_Price,
                    'qty_dgrsf_1' : qty_dgrsf_1,
                    'qty_dgrsf_2' : qty_dgrsf_2,
                    'prix_prom_dgrsf_1' : prix_prom_dgrsf_1,
                    'prix_prom_dgrsf_2' : prix_prom_dgrsf_2

                    }                
    

        


        if int(len(configs)) == 2:
            # print("*******************************************I am here")
            # url = response.request.url
            designation = product_detail.css('div.page-title-wrapper.product h1.page-title span[data-dynamic="product_name"]::text').get().strip()
            try:
                product_add_cart_form = response.css('div.product-add-form.configurable div.fieldset script[type="text/x-magento-init"]').getall()[0].strip()
            except:
                pass                
                
                product_detail = response.css('div.columns')

                reference = product_detail.css('div.product.attibute.code_mega.sku div.value[itemprop="sku"]::text').get()
            
            if reference is not None:
                reference = reference.strip()
                
            else:    
                reference = re.findall(r'Code article fournisseur :(.+?)<', product_add_cart_form)
                if len(reference) > 0:
                    reference = reference[0]
                else:    
                    reference = re.findall(r'\"code_mega\":\{\"(\d*)\":{\"id\":\"(\d*-\d*)\",\"value\":\"(\d*-\d*)\"},', product_add_cart_form)
                    if len(reference) > 0:
                        reference= reference[0][-1]
                    else:
                        reference = 'Not Found'
            
            
            marque = product_detail.css('span.product-brand a::attr(href)').get()

            if marque is not None :
                marque =  marque.split('/')[-1]
            else:
                marque = re.findall(r'\"marque\":{\"(.+?)\":{\"id\":\"(.+?)\",\"value\":\"(.+?)\"},', product_add_cart_form)
                
                if len(marque) > 0:
                    marque= marque[0][-1]
                else:
                    marque = 'Not Found'

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
            # print(product_options)
            

            prod_price = ast.literal_eval(product_options['option_prices'][0])

            attribute_1 = list(product_options.keys())[0]
            att_value_1 = list(product_options[attribute_1].keys())

            attribute_2 = list(product_options.keys())[1]
            att_value_2 = list(product_options[attribute_2].keys())

            prod_id_1 = list(product_options[attribute_1].values())

            chain = itertools.chain(*prod_id_1)
            flattened_list = list(chain)
            prod_id_1 = flattened_list

            prod_id_keys_2 = list(product_options[attribute_2].keys())
            prod_id_values_2 = list(product_options[attribute_2].values())

            prod_id_2_key_value = dict(zip(prod_id_keys_2, prod_id_values_2))

            prod_id_keys_1 = list(product_options[attribute_1].keys())
            prod_id_values_1 = list(product_options[attribute_1].values())

            prod_id_1_key_value = dict(zip(prod_id_keys_1, prod_id_values_1))

            prod_price = ast.literal_eval(product_options['option_prices'][0])


            for k,v in prod_id_2_key_value.items():
                for ky, ve in prod_id_1_key_value.items():
                    for i in range(0,len(v)):
                        for j in range(0, len(ve)):
                            if v[i] == ve[j]:
                                old_Price = prod_price[str(product_options[attribute_1][ky][j])]['oldPrice']['amount']
                                base_price = prod_price[str(product_options[attribute_1][ky][j])]['basePrice']['amount']
                                besttier_Price = prod_price[str(product_options[attribute_1][ky][j])]['besttierPrice']['amount']
                                final_price = prod_price[str(product_options[attribute_1][ky][j])]['finalPrice']['amount']
                                tier_price = prod_price[str(product_options[attribute_1][ky][j])]['tierPrices']

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
                                    'atribute1':attribute_1,
                                    'attribute_1_value': ky,
                                    'atribute2':attribute_2,
                                    'attribute_2_value': k,
                                    'atribute3':' ',
                                    'attribute_3_value': ' ',
                                    'prix_promo_unit': besttier_Price,
                                    'ref_price_unit': old_Price,
                                    'qty_dgrsf_1' : qty_dgrsf_1,
                                    'qty_dgrsf_2' : qty_dgrsf_2,
                                    'prix_prom_dgrsf_1' : prix_prom_dgrsf_1,
                                    'prix_prom_dgrsf_2' : prix_prom_dgrsf_2

                                    }   

        
        if int(len(configs)) == 3:
            # url = response.request.url
            designation = product_detail.css('div.page-title-wrapper.product h1.page-title span[data-dynamic="product_name"]::text').get().strip()
            
            try:
                product_add_cart_form = response.css('div.product-add-form.configurable div.fieldset script[type="text/x-magento-init"]').getall()[0].strip()
            except:
                pass                
            
            product_detail = response.css('div.columns')

            reference = product_detail.css('div.product.attibute.code_mega.sku div.value[itemprop="sku"]::text').get()
            
            if reference is not None:
                reference = reference.strip()
                
            else:    
                reference = re.findall(r'Code article fournisseur :(.+?)<', product_add_cart_form)
                if len(reference) > 0:
                    reference = reference[0]
                else:    
                    reference = re.findall(r'\"code_mega\":\{\"(\d*)\":{\"id\":\"(\d*-\d*)\",\"value\":\"(\d*-\d*)\"},', product_add_cart_form)
                    if len(reference) > 0:
                        reference= reference[0][-1]
                    else:
                        reference = 'Not Found'
            
            
            marque = product_detail.css('span.product-brand a::attr(href)').get()

            if marque is not None :
                marque =  marque.split('/')[-1]
            else:
                marque = re.findall(r'\"marque\":{\"(.+?)\":{\"id\":\"(.+?)\",\"value\":\"(.+?)\"},', product_add_cart_form)
                
                if len(marque) > 0:
                    marque= marque[0][-1]
                else:
                    marque = 'Not Found'

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
            # print(product_options)
            

            prod_price = ast.literal_eval(product_options['option_prices'][0])

            attribute_1 = list(product_options.keys())[0]
            att_value_1 = list(product_options[attribute_1].keys())

            attribute_2 = list(product_options.keys())[1]
            att_value_2 = list(product_options[attribute_2].keys())

            attribute_3 = list(product_options.keys())[2]
            att_value_3 = list(product_options[attribute_3].keys())

            prod_id_1 = list(product_options[attribute_1].values())

            chain = itertools.chain(*prod_id_1)
            flattened_list = list(chain)
            prod_id_1 = flattened_list

            prod_id_keys_1 = list(product_options[attribute_1].keys())
            prod_id_values_1 = list(product_options[attribute_1].values())

            prod_id_1_key_value = dict(zip(prod_id_keys_1, prod_id_values_1))

            prod_id_keys_2 = list(product_options[attribute_2].keys())
            prod_id_values_2 = list(product_options[attribute_2].values())

            prod_id_2_key_value = dict(zip(prod_id_keys_2, prod_id_values_2))

            prod_id_keys_3 = list(product_options[attribute_3].keys())
            prod_id_values_3 = list(product_options[attribute_3].values())

            prod_id_3_key_value = dict(zip(prod_id_keys_3, prod_id_values_3))

            prod_price = ast.literal_eval(product_options['option_prices'][0])


            for k,v in prod_id_2_key_value.items():
                for ky, ve in prod_id_1_key_value.items():
                    for ke, va in prod_id_3_key_value.items():
                        for i in range(0,len(v)):
                            for j in range(0, len(ve)):
                                for l in range(0, len(va)):
                                    if v[i] == ve[j] and v[i] == va[l] and ve[j] == va[l]:
                                        old_Price = prod_price[str(product_options[attribute_1][ky][j])]['oldPrice']['amount']
                                        base_price = prod_price[str(product_options[attribute_1][ky][j])]['basePrice']['amount']
                                        besttier_Price = prod_price[str(product_options[attribute_1][ky][j])]['besttierPrice']['amount']
                                        final_price = prod_price[str(product_options[attribute_1][ky][j])]['finalPrice']['amount']
                                        tier_price = prod_price[str(product_options[attribute_1][ky][j])]['tierPrices']

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
                                            'atribute1':attribute_1,
                                            'attribute_1_value': ky,
                                            'atribute2':attribute_2,
                                            'attribute_2_value': k,
                                            'atribute3':attribute_3,
                                            'attribute_3_value': ke,
                                            'prix_promo_unit': besttier_Price,
                                            'ref_price_unit': old_Price,
                                            'qty_dgrsf_1' : qty_dgrsf_1,
                                            'qty_dgrsf_2' : qty_dgrsf_2,
                                            'prix_prom_dgrsf_1' : prix_prom_dgrsf_1,
                                            'prix_prom_dgrsf_2' : prix_prom_dgrsf_2

                                            }   

  


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Megadental2Spider)
    process.start()