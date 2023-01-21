import logging

from src.config import Config
from src.market import MarketItem, MarketAPI, MarketBuyError
from src.market.api import parse_search_data
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
        category, params = parse_search_data(search_url)
        searches.append((category, params))

    while True:
        for search, params in searches:
            search_result = market.search(search, params)
            items = search_result.get('items', [])

            logging.info(
                f'По запросу {search} с параметрами {params} найдено {len(items)} аккаунтов'
            )

            for item in items:
                item_id = item["item_id"]
                market_item = MarketItem(item, lolzteam_token)
                try:
                    logging.info(f'Покупаю аккаунт {item_id}')
                    market_item.fast_buy()
                except MarketBuyError as error:
                    logging.warning(
                        f'При попытке покупки аккаунта {item_id} произошла ошибка: {error.message}'
                    )
                    continue
                else:
                    logging.info(f'Аккаунт {item_id} успешно куплен!')
                    count_purchase += 1
                    account_object = market_item.item_object
                    seller = account_object['seller']
                    telegram.send_message(
                        f"👷 Приобретен аккаунт: <a href=\"https://lzt.market/{item_id}\">"
                        f"{account_object['title']}</a>\n"
                        f"💲 Цена: <code>{account_object['price']}₽</code>\n"
                        f"👷 Продавец: <a href=\"https://zelenka.guru/members/{seller['user_id']}\">"
                        f"{seller['username']}</a>",
                        config.telegram.id,
                        parse_mode='HTML'
                    )

                    if count_purchase >= config.lolzteam.count:
                        logging.info(
                            f'Успешно куплено {count_purchase} аккаунтов, работа завершена.')
                        exit()
                    break


if __name__ == '__main__':
    main()
