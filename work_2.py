import requests
from bs4 import BeautifulSoup
import json

# Отправляем GET-запрос к указанному URL
url = 'http://books.toscrape.com/'
response = requests.get(url)

# Получаем содержимое страницы
page_content = response.content

# Создаем объект BeautifulSoup для работы с HTML
soup = BeautifulSoup(page_content, 'html.parser')

# Находим все ссылки на категории
category_links = soup.select('.side_categories ul li ul li a')


# Создаем пустой список для хранения данных о книгах
books_data = []

# Перебираем все ссылки на категории и скрапим данные о книгах
for category_link in category_links:
    category_url = url + category_link['href']
    category_response = requests.get(category_url)
    category_page_content = category_response.content
    category_soup = BeautifulSoup(category_page_content, 'html.parser')

    # Находим все ссылки на книги
    book_links = category_soup.select('.image_container a')
    #print(book_links)

    # Перебираем все ссылки на книги и извлекаем нужные данные
    for book_link in book_links:
        book_url = url + 'catalogue/' + book_link['href']
        book_response = requests.get(book_url)
        book_page_content = book_response.content
        book_soup = BeautifulSoup(book_page_content, 'html.parser')

        # Извлекаем данные о книге
        title_element = book_soup.select_one('.product_main h1')
        title = title_element.text.strip() if title_element else None
        

        price_element = book_soup.select_one('.price_color')
        price = price_element.text.strip()[1:] if price_element else None
        print(price)

        stock_element = book_soup.select_one('.availability')
        stock = int(stock_element.text.strip().split()[2]) if stock_element else None
        print(stock)

        description_element = book_soup.select_one('#product_description + p')
        description = description_element.text.strip() if description_element else None
        print(description)
        # Создаем словарь с данными о книге и добавляем его к списку
        book_data = {
            'title': title,
            'price': price,
            'stock': stock,
            'description': description
        }
        books_data.append(book_data)

# Сохраняем данные в JSON-файл
with open('books_data.json', 'w') as file:
    json.dump(books_data, file)
