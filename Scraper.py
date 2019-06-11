from bs4 import BeautifulSoup
import requests
import re
import csv


def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)


def get_links(page_number):
    url = "http://books.toscrape.com/catalogue/page-" + \
        str(page_number) + ".html"
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    all_links = soup.findAll('section')
    return all_links


def get_page_titles(all_links, titles):
    for li in all_links:

        idk = li.findAll("h3")
        idk2 = li.findAll("div", {"class": "product_price"})
        prices = [i.find("p", {"class": "price_color"}) for i in idk2]

        count = 0
        for i in idk:
            title = i.find("a").get("title")
            price = prices[count]
            price = remove_tags(str(price))[1:]

            book_details = [str(title), price]
            titles.append(book_details)

            count += 1


def main():
    titles = []

    for i in range(1, 51):
        all_links = get_links(i)
        get_page_titles(all_links, titles)

    with open('books.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(titles)
    csvFile.close()


main()
