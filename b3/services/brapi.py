import requests
import logging
import json

from b3.models import Search, StockPrice


class BRAPIService:
    quote_url = "https://brapi.dev/api/quote/"
    token = "gGZMMDMBqzLjmUCMVHGqUV"

    def handle(self, search: Search):
        api_results = self.__get_api_results(search=search)

        stock_prices = []
        for data in api_results:

            price = self.__get_price(tunnel=search.price_tunnel, stock=data["result"])
            stock_prices.append(StockPrice(
                search=search,
                stock_id=data["stock_id"],
                price=price,
            ))

        StockPrice.objects.bulk_create(stock_prices, batch_size=100)

    def __get_api_results(self, search: Search) -> dict:
        params = {
            'range': '5d',
            'interval': '1d',
            'token': self.token,
        }

        stock_results = []
        for stock in search.stocks.all():
            try:
                response = requests.get(
                    self.quote_url + stock.code,
                    params=params,
                )
                response.raise_for_status()
                stock_results.append(
                    {
                        "stock_id": stock.id,
                        "result": response.json()["results"][0],
                    }
                )

            except:
                logging.error(json.loads(response.content))

        return stock_results


    def __get_price(self, tunnel: str, stock: dict) -> float:
        match tunnel:
            case Search.SUPERIOR:
                return stock["regularMarketDayHigh"]

            case Search.NEGOCIOS:
                return stock["regularMarketPrice"]

            case Search.INFERIOR:
                return stock["regularMarketDayLow"]
