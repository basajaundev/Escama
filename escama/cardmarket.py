import configparser
import json
import os

from mkmsdk.api_map import _API_MAP
from mkmsdk.mkm import Mkm


class CardMarket:
    def __init__(self):
        self.mkm = Mkm(_API_MAP["1.1"]["api"], _API_MAP["1.1"]["api_root"])
        self.read_conf()

    @staticmethod
    def read_conf():
        escama_conf = configparser.ConfigParser()
        escama_conf.read('escama.conf')
        os.environ['MKM_APP_TOKEN'] = escama_conf.get('MKMConf', 'appToken')
        os.environ['MKM_APP_SECRET'] = escama_conf.get('MKMConf', 'appSecret')
        os.environ['MKM_ACCESS_TOKEN'] = escama_conf.get('MKMConf', 'accessToken')
        os.environ['MKM_ACCESS_TOKEN_SECRET'] = escama_conf.get('MKMConf', 'accessSecret')

    def get_username(self):
        resp = self.mkm.account_management.account()
        json_data = json.dumps(resp.json()['account'])
        data = json.loads(json_data)
        username = data.get('username')
        return username

    def get_idproduct(self, card, exp_name):
        id_product = None
        resp = self.mkm.market_place.products(name=card, game=1, language=1, match='true')
        json_data = json.dumps(resp.json())
        data = json.loads(json_data)
        for prod in data.get('product'):
            if prod['expansion'] == exp_name:
                id_product = prod['idProduct']
        return id_product

    def get_productstock(self, idprod):
        stock = None
        username = self.get_username()
        resp = self.mkm.market_place.articles_user(user=username)
        json_data = json.dumps(resp.json())
        data = json.loads(json_data)
        for art in data.get('article'):
            if art['idProduct'] == idprod:
                stock = art['count']
        return stock

    def get_productprice(self, idprod):
        resp = self.mkm.market_place.product(product=idprod)
        json_data = json.dumps(resp.json()['product'])
        data = json.loads(json_data)
        data_price_raw = json.dumps(data.get('priceGuide'))
        data_price = json.loads(data_price_raw)
        return data_price.get('LOWEX')

    def get_foilprice(self, idprod):
        resp = self.mkm.market_place.product(product=idprod)
        json_data = json.dumps(resp.json()['product'])
        data = json.loads(json_data)
        data_price_raw = json.dumps(data.get('priceGuide'))
        data_price = json.loads(data_price_raw)
        return data_price.get('LOWFOIL')

    def sell_card(self, data, stock):
        if stock == 0:
            self.mkm.stock_management.post_stock(data=data)  # Añadir nueva carta
        else:
            self.mkm.stock_management.put_stock(data=data)  # Añadir carta al stock

