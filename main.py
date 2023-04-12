import sys
import time

from avito import Avito
import telegram
from exceptions import UnsuitableProductError
from loguru import logger
from loader import db_handler

def main():
    avito_service = Avito()
    while True:
        categories = db_handler.get_categories()
        time.sleep(1)
        for url in categories:
            offers_urls = avito_service.get_urls(url[0])
            black_list = db_handler.get_blacklist()
            stop_words = db_handler.get_stopwords()

            if offers_urls:
                for offer_url in offers_urls:
                    try:
                        offer = avito_service.get_info(offer_url, stop_words, black_list, url[0])
                    except UnsuitableProductError:
                        logger.debug(f'Will be skipped - {offer_url}')
                    else:
                        telegram.send_offer(offer)

                    db_handler.add_to_viewed_links(offer_url)
                    time.sleep(3)
            else:
                time.sleep(5)

if __name__ == '__main__':
    main()