images = []
for book in books:
    img_alt = f"{book['author']} - {book['title']}"
    img_link = soup.find('img', alt=img_alt)['data-pagespeed-lazy-src']
    print(img_alt, '\n', img_link, '\n')
    book['coverImageUrl'] = img_link
    images.append(img_link)