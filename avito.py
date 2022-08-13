from random import choice

from bs4 import BeautifulSoup
from chrome import Chrome
import requests, time, csv, random, re
from offer import AvitoOffer
from loguru import logger
from exceptions import UnsuitableProductError
from loader import db_handler

host = 'https://www.avito.ru'


def stopwatch(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        logger.info(f'Функция {func.__name__} отработала за {int(time.time() - start_time)} секунд')
        return result

    return wrapper


class Avito:
    def __init__(self):
        with open('UserAgents.txt', 'r', encoding='utf-8') as f:
            self.user = choice([user.strip() for user in f.readlines()])
        self.chrome = Chrome(self.user)

    @stopwatch
    def get_urls(self, url):
        logger.debug(f'Collecting urls from the category - {url}')
        page = 1

        products_urls = []

        # while True:
        #     logger.debug(f'Parsing page number: {page}')
        #
        #     if page == 1:
        #         content = self.chrome.get_html(url)
        #     else:
        #         if '?' not in url:
        #             url += '?'
        #
        #         content = self.chrome.get_html(url=f'{url}&p={page}')

        content = self.chrome.get_html(url)
        soup = BeautifulSoup(content, 'lxml')

        # try:
        #     pagination_div = soup.find_all('div', {'data-marker': 'pagination-button'})[0]
        # except IndexError:
        #     max_page = 1
        #     logger.debug(f'Max page in category: {max_page}')
        # else:
        #     max_page = int(pagination_div.find_all('span')[-2].text)
        #
        #     logger.debug(f'Max page in category: {max_page}')

        urls_containers = soup.find_all('a', class_='iva-item-sliderLink-uLz1v')

        for a in urls_containers:
            products_urls.append(host + a.get('href'))

        # if page >= max_page:
        #     break

        # page += 1
        # time.sleep(random.uniform(2.0, 5.0))

        products_urls = list(set(products_urls))

        viewed_links = db_handler.get_viewed_links()
        for url in viewed_links:
            try:
                products_urls.remove(url)
            except ValueError:
                pass
            else:
                logger.debug(f'Will be skipped - {url}')

        logger.debug(f'Urls from the category are collected. New urls found: {len(products_urls)}')
        return products_urls

    @stopwatch
    def get_info(self, url, stop_words=[], black_list=[]) -> AvitoOffer:

        logger.debug(f'Parsing offer - {url}')

        content = self.chrome.get_html(url)
        with open('last_page.html', 'w', encoding='utf-8') as f_o:
            f_o.write(content)

        offer = AvitoOffer(url)
        soup = BeautifulSoup(content, 'lxml')

        try:
            offer.seller_url = soup.find_all('div', {'data-marker': 'seller-info/name'})[0].find('a').get('href')

        except Exception:
            offer.seller_url = None

        else:
            logger.debug(f'Seller url found: {offer.seller_url}')
            for user in black_list:
                if user.strip() in offer.seller_url:
                    logger.debug(f'User in blacklist: {user}')

                    raise UnsuitableProductError

        # print('seller url:', offer.seller_url)
        try:
            offer.title = soup.find_all('span', class_='title-info-title-text')[0].text
        except IndexError:
            raise UnsuitableProductError
        # print('title:', offer.title)

        try:
            offer.description = soup.find_all('div', {'itemprop': 'description'})[0].text

            if len(offer.description) > 3500:
                offer.description = offer.description[:1000]

            # print('description:', offer.description)
        except IndexError:
            # print('Описание не найдено')
            raise UnsuitableProductError
            # print('description:', offer.description)

        for word in stop_words:

            if word.lower() in offer.title.lower() or word.lower() in offer.description.lower():
                logger.debug(f'Stop word was found: {word}')
                raise UnsuitableProductError

        try:
            offer.price = soup.find_all('span', class_='js-item-price')[0].text
            # print('price:', offer.price)
        except IndexError:
            # print('price:', offer.price)
            pass

        # offer.id = soup.find_all('span', {'data-marker': 'item-view/item-id'})[0].text.replace('№ ', '')
        # print('id', offer.id)

        try:
            offer.photo = soup.find_all('div', {'class': re.compile(r'^image-frame-wrapper')})[0].get('data-url')
        except Exception:
            try:
                offer.photo = soup.find_all('div', {'class': re.compile(r'^gallery-img-frame')})[0].get('data-url')

            except IndexError:
                raise UnsuitableProductError

        logger.debug(f'The offer was parsed - {url}')
        return offer

    def quit(self):
        self.chrome.quit()
