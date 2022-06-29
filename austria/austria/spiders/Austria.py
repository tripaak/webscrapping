import scrapy
import csv
import requests
import os
from bs4 import BeautifulSoup as bs4

## Function fetch hidden information


def get_hidden_details(town_id, col):
    get_info = requests.post("https://fre.cityhallworldwide.com/accion/directory.bd.asp",
                             data={'accion': 'getInformation',
                                   'idinformation': town_id,
                                   'colum': col
                                   })
    soup = bs4(get_info.content, "lxml")

    if col == 'website':
        try:
            if get_info.text == 'Information non disponible':
                return get_info.text
            else:
                return soup.findAll('a')[0].get('href')
        except:
            return 'Information non disponible'
    else:
        return get_info.text


class AustriaSpider(scrapy.Spider):
    name = 'Austria'
    allowed_domains = ['fre.cityhallworldwide.com']
    start_urls = ['https://fre.cityhallworldwide.com/mairie-en-autriche-pag-1/']

    def parse(self, response):
        urls = response.css('div.region a::attr(href)').getall()
        for url in urls:
            yield scrapy.Request('https://' + self.allowed_domains[0] + url[:-1] + '-pag-1',
                             callback=self.parse_province)

    def parse_province(self, response):
        url_province = response.css('div.region a::attr(href)').getall()
        for url in url_province:
            yield scrapy.Request('https://' + self.allowed_domains[0] + url, callback=self.parse_towns)

    def parse_towns(self, response):
        towns = response.css('div.information_linea a::attr(href)').getall()
        for url in towns:
            if '/mairie-en-autriche/' in url:
                yield scrapy.Request('https://' + self.allowed_domains[0] + url, callback=self.extract_town_info)

    def extract_town_info(self, response):
        key = response.css('div.information_col1::text').getall()
        value = response.css('div.information_col2::text').getall()
        town_id = response.css('input[id=idinformation]').attrib['value']
        town_data = {'Url': response.url}
        print(town_data)

        for i in range(len(key)):
            town_data[key[i]] = value[i]

        for key in town_data.keys():
            if key == 'Téléphone':
                town_data[key] = get_hidden_details(town_id, 'phone')
            if key == 'Email':
                town_data[key] = get_hidden_details(town_id, 'email')
            if key == 'Site':
                town_data[key] = get_hidden_details(town_id, 'website')

        file_exist = os.path.exists('town_all_austria.csv')

        with open('town_all_austria.csv', 'a', newline='') as file:
            fieldnames = ['Url', 'Pays', 'Etat', 'Province', 'Ville', 'Nom', 'Adresse', 'Postal', 'Téléphone', 'Email',
                          'Site', 'GPS']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exist:
                writer.writeheader()
            else:
                writer.writerow(town_data)
