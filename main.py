import logging

from src.base import MarketBuyError
from src.config import Config
from src.market import MarketItem, MarketAPI
from src.telegram import TelegramAPI


def main():
    config = Config.load_config('config.ini')
    logging.basicConfig(level=config.logging.level, format=config.logging.format)
    lolzteam_token = config.lolzteam.token

    telegram = TelegramAPI(config.telegram.bot_token)
    market = MarketAPI(lolzteam_token)
    count_purchase = 0
    searches = []
    for search_url in config.lolzteam.search_urls_list:
        category, params = market.parse_search_data(search_url)
        searches.append((category, params))

    while True:
        for search, params in searches:
            search_result = market.search(search, params)
            items = search_result.get('items', [])

            logging.info(f'По запросу {search} с параметрами {params} найдено {len(items)} аккаунтов')

            for item in items:
                if count_purchase >= config.lolzteam.count:
                    logging.info(f'Успешно куплено {count_purchase} аккаунтов, работа завершена.')
                    exit()

                item_id = item["item_id"]
                market_item = MarketItem(item, lolzteam_token)
                try:
                    market_item.buy()
                except MarketBuyError as error:
                    logging.info(f'При попытке покупки аккаунта {item_id} произошла ошибка: {error.message}')
                    continue
                else:
                    count_purchase += 1
                    telegram.send_message(config.telegram.text_message, config.telegram.id)
                    break


if __name__ == '__main__':
    main()
