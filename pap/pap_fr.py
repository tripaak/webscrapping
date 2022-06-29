# we scrapp PAP fr website
from bs4 import BeautifulSoup
import requests


html_text = requests.get('https://www.pap.fr/annonce/vente-appartements-bougival-78380-g39135', headers={'User-Agent': 'Mozilla/5.0'}).text
soup = BeautifulSoup(html_text, 'lxml')
main = soup.find('div', class_='row row-large-gutters page-item')
properties = main.find_all('div', class_='col-1-3')
for prop in properties:
    # type_of_ad = prop.find('div', class_='item-tag').span.text
    location = prop.find('div', class_='item-body').a.find('span', class_='h1', recursive=False).text.strip()
    price = prop.find('span', class_='item-price').text
    description = prop.find('p', class_='item-description').text.strip()
    # print(type_of_ad)
    print(location)
    print(price)
    print(description)
    with open('data/pap_fr_details.text', 'a') as f:
        # f.write(type_of_ad)
        f.write(location)
        f.write(price)
        f.write(description)
        f.write('\n')
