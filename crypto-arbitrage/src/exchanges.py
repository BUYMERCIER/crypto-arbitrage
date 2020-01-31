#!/usr/bin/env python3

#
# fetches the market price from the exchanges
#

import requests
from .rates import eur_equivalent


class Exchange:
    base_endpoint = ''
    post_url = ''
    base_currency = ''
    json_rate_arg = ''  # e.g. 'ask' or 'last'
    params = False  # if request requires parameters

    def get_rate(self, crypto):
        if self.params:
            r = requests.get(self.base_endpoint, params={'currency': crypto})
        else:
            r = requests.get(self.base_endpoint +
                             crypto.lower() + self.post_url)
        r.raise_for_status()
        data = r.json()
        rate_base_currency = float(data[self.json_rate_arg])
        if self.base_currency.upper() != 'EUR':
            rate = rate_base_currency / eur_equivalent(self.base_currency)
        else:
            rate = rate_base_currency
        return rate


class Korbit(Exchange):
    base_endpoint = 'https://api.korbit.co.kr/v1/ticker?currency_pair='
    post_url = '_krw'
    base_currency = 'KRW'
    json_rate_arg = 'last'


class Coinone(Exchange):
    base_endpoint = 'https://api.coinone.co.kr/ticker/'
    base_currency = 'KRW'
    json_rate_arg = 'last'
    params = True


class CoinbasePro(Exchange):
    base_endpoint = 'https://api.pro.coinbase.com/products/'
    post_url = '-EUR/ticker'
    base_currency = 'EUR'
    json_rate_arg = 'ask'


def bittrex(currency_in):
    """ Returns the value of 1 currency_in according to bittrex """
    bittrex_endpoint = ('https://bittrex.com/api/v1.1/public'
                        '/getticker?market=')
    req = requests.get(bittrex_endpoint + "usd-" + currency_in.upper())
    price_json = req.json()
    price = float(price_json['result']['Last'])
    return price


def cryptonator(currency_in, market):
    req = requests.get("https://api.cryptonator.com/api/full/" +
                       currency_in.lower() + "-eur")
    req.raise_for_status()
    callback = req.json()
    markets = callback['ticker']['markets']
    if market == 'bitfinex':
        return markets[0]['price']
    if market == 'cexio':
        return markets[1]['price']
    if market == 'exmo':
        return markets[2]['price']
    if market == 'kraken':
        return markets[3]['price']
    if market == 'livecoin':
        return markets[4]['price']
    if market == 'wexnz':
        return markets[5]['price']
    return False

###############################################################################
#
# ADD MARKETS APIs HERE
#
