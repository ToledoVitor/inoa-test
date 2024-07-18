import requests
import logging
import json

from b3.models import Search, StockPrice, Stock


class BRAPIService:
    quote_url = "https://brapi.dev/api/quote/"
    token = "gGZMMDMBqzLjmUCMVHGqUV"

    def handle(self, search: Search):
        results = self.__get_api_results(search=search)

        stock_prices = []
        for result in results:
            stock = Stock.objects.get(code=result["symbol"])

            match search.price_tunnel:
                case search.LAST_TRADED_PRICE:
                    stock_prices.append(StockPrice(
                        search=search,
                        stock=stock,
                        price=result["regularMarketPrice"],
                    ))

                case search.C_LAST:
                   stock_prices.append(StockPrice(
                        search=search,
                        stock=stock,
                        price=result["regularMarketPrice"],
                    ))

                case search.MOST_RECENT:
                   stock_prices.append(StockPrice(
                        search=search,
                        stock=stock,
                        price=result["regularMarketPrice"],
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
                    response.json()["results"][0]
                )

            except:
                logging.error(json.loads(response.content))

        return stock_results
