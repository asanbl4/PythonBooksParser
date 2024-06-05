from bs4 import BeautifulSoup
import requests
import psycopg2
import random

table_name = 'books'

conn = psycopg2.connect(
    database='books',
    host='localhost',
    user='postgres',
    password='postgres',
    port='5432'
)
cursor = conn.cursor()


URL = "https://www.livelib.ru/books/top"
number_of_books = 97

response = requests.get(url=URL)
soup = BeautifulSoup(response.content, 'html.parser')
authors = [name.get_text() for name in soup.find_all('a', class_='book-item__author')]
titles = [title.get_text() for title in soup.find_all('a', class_='book-item__title')]
year_rows = soup.find_all('td', string='Год издания:')
years = [year_row.find_next_sibling('td').text for year_row in year_rows]
descriptions = [description.get_text(strip='\n') for description in soup.find_all('div', class_='book-item-desc')]
images = [f"{a_tag.find('img').get('data-pagespeed-lazy-src')}" for a_tag in soup.find_all('a', class_='book-item__link')]

books = []
for i in range(number_of_books):
    books.append({
        'title': titles[i],
        'author': authors[i],
        'year': years[i],
        'description': descriptions[i],
        'coverImageUrl': images[i]
        })

try:
    for book in books:
        query = f"""
                INSERT INTO {table_name} 
                ("title", "description", "price", "author", "coverImageUrl", "year") 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
        cursor.execute(query, (
            book['title'],
            book['description'],
            random.randint(70, 120) * 10,
            book['author'],
            book['coverImageUrl'],
            book['year']
        ))
    conn.commit()
except Exception as e:
    print(e)
    conn.rollback()
finally:
    conn.close()

conn.close()