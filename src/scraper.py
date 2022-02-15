import csv
import os

import requests
from bs4 import BeautifulSoup
import pandas as pd

from image_helper import ImageHelper
from storage_helper import StorageHelper


# creation class Scraper
class Scraper:
    SRC_ATTRIBUTE: str = 'src'
    BOOKS_TO_SCRAPE_BASE_URL: str = 'https://books.toscrape.com/'
    CATALOGUE_URL: str = f'{BOOKS_TO_SCRAPE_BASE_URL}catalogue/'
    LXML: str = 'lxml'
    A_TAG: str = 'a'
    TR_TAG: str = 'tr'
    P_TAG: str = 'p'
    IMG_TAG: str = 'img'
    H1_TAG: str = 'h1'

    # definition instance ds variable intanciée

    def __init__(self, storage_helper: StorageHelper, image_helper: ImageHelper):
        self.storage_helper: StorageHelper = storage_helper
        self.image_helper: ImageHelper = image_helper

    def _get_page(self, url: str):
        page = requests.get(url)
        status = page.status_code
        soup = BeautifulSoup(page.text, Scraper.LXML)
        return [soup, status]

    def _get_links(self, soup) -> [str]:
        links: [str] = []
        listings = soup.find_all(class_="product_pod")
        for listing in listings:
            bk_link = listing.find("h3").a.get("href")
            cmplt_link = f'{Scraper.CATALOGUE_URL}{bk_link}'
            links.append(cmplt_link)
        return links

    def _extract_img_src_attribute(self, img_tag) -> str:
        if hasattr(img_tag, Scraper.SRC_ATTRIBUTE):
            relative_img_path: str = img_tag[Scraper.SRC_ATTRIBUTE].replace('../../', '')
            return f"{Scraper.BOOKS_TO_SCRAPE_BASE_URL}{relative_img_path}"
        return ''

    def _extract_info(self, links):
        all_books = []
        # Extract info from each link
        for link in links:
            res = requests.get(link).text
            book_soup = BeautifulSoup(res, Scraper.LXML)

            title = [book_soup.find(Scraper.H1_TAG).get_text()]
            product_page_url = [link]
            universal_product_code = [book_soup.find_all(Scraper.TR_TAG)[0].get_text()]
            price_including_tax = [book_soup.find_all(Scraper.TR_TAG)[3].get_text()]
            price_excluding_tax = [book_soup.find_all(Scraper.TR_TAG)[2].get_text()]
            number_available = [book_soup.find_all(Scraper.TR_TAG)[5].get_text()]
            product_description = [book_soup.find_all(Scraper.P_TAG)[3].get_text()]
            category = [book_soup.find_all(Scraper.A_TAG)[3].get_text()]
            review_rating = [book_soup.find_all(Scraper.TR_TAG)[6].get_text()]
            image_url = self._extract_img_src_attribute(book_soup.find_all(Scraper.IMG_TAG)[0])
            self.image_helper.download_img(image_url)
            book = {'title': title, 'product_page_url': product_page_url,
                    'universal_product_code': universal_product_code,
                    'price_including_tax': price_including_tax, 'price_excluding_tax': price_excluding_tax,
                    'number_available': number_available, 'product_description': product_description,
                    'category': category, 'review_rating': review_rating, 'image_url': image_url}

            all_books.append(book)
            self._save_csv(book)

        df = pd.DataFrame(all_books)
        print(df)

    def _save_csv(self, book):
        # create csv file with book data
        header = book.keys()
        csv_storage_path = os.path.join(self.storage_helper.csv_storage_path.strip(), 'data_csv')
        filename = csv_storage_path.strip()

        if os.path.isfile(filename):
            with open(filename, 'a', newline='', encoding='utf-8') as output_file:
                writer = csv.DictWriter(output_file, fieldnames=header)
                writer.writerow(book)
        else:
            with open(filename, 'w') as output_file:
                writer = csv.DictWriter(output_file, fieldnames=header)
                writer.writeheader()
                writer.writerow(book)

    def run(self):
        pg = 1
        while True:
            url = f"{Scraper.CATALOGUE_URL}page-{pg}.html"
            soup_status = self._get_page(url)
            if soup_status[1] == 200:
                print(f"scraping page {pg}")
                links: [str] = self._get_links(soup_status[0])
                self._extract_info(links)
                pg += 50
            else:
                print("The End")
                break

