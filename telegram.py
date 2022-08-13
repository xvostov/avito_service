from offer import AvitoOffer as Offer
from settings import telegram_api_address, bot_api_token
from loguru import logger
import requests


def send_offer(offer: Offer):
    resp = requests.post(f'http://{telegram_api_address}/offer', json={
        'token': bot_api_token,
        'url': offer.url,
        'title': offer.title,
        'id': offer.id,
        'description': offer.description,
        'price': offer.price,
        'img_url': offer.photo
    }, timeout=1)

    if resp.status_code != 200:
        raise logger.error(f'Invalid server response: {resp.status_code}')

class AvitoOffer:
    def __init__(self, url):
        self.url = url
        self.id = None
        self.title = None
        self.price = None
        self.number = None
        self.seller_name = None
        self.all_views = None
        self.today_views = None
        self.date = None
        self.description = None
        self.photo = None
        self.seller_url = None