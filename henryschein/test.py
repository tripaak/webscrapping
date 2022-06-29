import requests
import scrapy

script = {
    '@context': 'http://schema.org/', 
    '@type': 'Product', 
    'name': 'Aiguilles anesthésie Intraligamentaires CYBERTECH - 30g S - 0.30x13mm - Boîte de 100', 
    'description': 'Aiguilles &agrave;&nbsp; anesth&eacute;sie intraligamentaires', 
    'sku': '900-6527', 
    'image': 'https://www.henryschein.fr/fr-fr/images/shared/imageNotAvailable_600x600.png', 
    'brand': {
        '@type': 'Organization', 
        'name': 'CYBERTECH'}, 
    'url': 'https://www.henryschein.fr/fr-fr/dental/p/anesthesie-pharmacie/aiguilles/aiguilles-anesthesie-intraligamentaires-cybertech-30g-s-0-30x13mm-boite-de-100/900-6527?promocode=7&FullPageMode=true', 
    'offers': 
            {'@type': 'Offer', 
            'priceCurrency': 'EUR', 
            'price': '16.99'}, 
    'mpn': '4A001882'}


url = script['url']
marque = script['brand']['name'] 
id_variante = script['sku'] 
designation = script['name']
description = script['description'] 
code_article =   script['mpn']
reference = script['sku']
sku = script['sku']
prix_reference_unit = script['offers']['price']

print(url)
print(marque)
print(id_variante)
print(designation)
print(description)
print(code_article)
print(reference)
print(prix_reference_unit)
# print(url)
# print(url)
# print(url)
# print(url)


