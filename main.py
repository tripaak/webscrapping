import time
from bs4 import BeautifulSoup
import requests
import csv


def my_scraping():
    html_text = requests.get('https://bookshop.org/books?keywords=python').text
    # print(html_text)
    soup = BeautifulSoup(html_text, 'lxml')
    # print(soup.prettify())
    books = soup.find_all('div', class_='booklist-book')
    books_list = []
    for book in books:
        # print(books)
        title = book.h2.a.text
        # print(title)
        author = book.h3.text.strip()
        # print(author)
        price = book.find('div', class_='pb-4 self-start text-s').div.text.strip()
        # print(price)
        # print('\n')
        books_list.append({'title': title, 'author': author, 'price': price})
    return books_list


def write_data_csv(data_list):
    with open('data/data.csv', 'w', newline='') as f:
        field_names = ['title', 'author', 'price']   # nothing but keys
        csv_writer = csv.DictWriter(f, fieldnames=field_names)
        csv_writer.writeheader()
        for element in data_list:
            csv_writer.writerow(element)


if __name__ == '__main__':
    scrap_data = my_scraping()
    write_data_csv(scrap_data)

