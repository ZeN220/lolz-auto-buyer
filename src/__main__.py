import logging

from src.config import Config
from src.market import MarketAPI, MarketBuyError, MarketItem
from src.market.api import parse_search_data
from src.telegram import TelegramAPI

TELEGRAM_MESSAGE = (
    '👷 Приобретен аккаунт: <a href="https://lzt.market/{item_id}">'
    "{title}</a>\n"
    "💲 Цена: <code>{price}₽</code>\n"
    '👷 Продавец: <a href="https://zelenka.guru/members/{seller_id}">'
    "{seller_username}</a>"
)


def main():
    config = Config.load_config("config.ini")
    logging.basicConfig(
        level=config.logging.level,
        format=config.logging.format,
    )
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
            items = search_result.get("items", [])

            logging.info(
                "По запросу %s с параметрами %s найдено %s аккаунтов",
                search,
                params,
                len(items),
            )

            for item in items:
                item_id = item["item_id"]
                market_item = MarketItem(item, lolzteam_token)
                try:
                    logging.info("Покупаю аккаунт %s", item_id)
                    market_item.fast_buy()
                except MarketBuyError as error:
                    logging.warning(
                        "При попытке покупки аккаунта %s произошла ошибка: %s",
                        item_id,
                        error.message,
                    )
                    continue
                else:
                    logging.info("Аккаунт %s успешно куплен!", item_id)
                    count_purchase += 1

                    account_object = market_item.item_object
                    seller = account_object["seller"]
                    telegram.send_message(
                        TELEGRAM_MESSAGE.format(
                            item_id=item_id,
                            title=account_object["title"],
                            price=account_object["price"],
                            seller_id=seller["seller_id"],
                            seller_username=seller["username"],
                        ),
                        config.telegram.id,
                        parse_mode="HTML",
                    )

                    if count_purchase >= config.lolzteam.count:
                        logging.info(
                            "Успешно куплено %s аккаунтов, работа завершена.",
                            count_purchase,
                        )
                        exit()
                    break


if __name__ == "__main__":
    main()
