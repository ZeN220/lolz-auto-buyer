import logging

from src.config import Config
from src.market import MarketItem, MarketAPI
from src.telegram import TelegramAPI


def main(
        lolzteam_token: str, telegram_token: str, telegram_id: int,
        text: str, search_url: str, count_accounts: int
):
    telegram = TelegramAPI(telegram_token)
    market = MarketAPI(lolzteam_token)
    category, params = market.parse_search_data(search_url)
    count_purchase = 0

    while True:
        search_result = market.search(category, params)
        if search_result:
            items = search_result['items']
            logging.info(f'По вашему запросу найдено {len(items)} аккаунтов')

            for item in items:
                while count_purchase < count_accounts:
                    item_id = item['item_id']
                    market_item = MarketItem(item, lolzteam_token)

                    # Говнокод из тонны условий / Shit code from too many conditions
                    logging.info(f'Бронирую аккаунт {item_id}...')
                    reserve = market_item.reserve()
                    reserve_errors = reserve.get('errors')
                    if reserve_errors:
                        logging.info(f'При попытке бронирования возникла ошибка: {reserve_errors[0]}')
                        market_item.cancel_reserve()
                        break

                    logging.info(f'Проверяю аккаунт {item_id}...')
                    check_account = market_item.check()
                    check_account_errors = check_account.get('errors')
                    if check_account_errors:
                        logging.info(f'При попытке проверки аккаунта возникла ошибка: {check_account_errors[0]}')
                        market_item.cancel_reserve()
                        break

                    logging.info(f'Покупаю аккаунт {item_id}...')
                    buy_account = market_item.confirm_buy()
                    buy_account_errors = buy_account.get('errors')
                    if buy_account_errors:
                        logging.info(f'При попытке покупки аккаунта возникла ошибка: {buy_account_errors[0]}')
                        market_item.cancel_reserve()
                        break

                    count_purchase += 1
                    telegram.send_message(text, telegram_id)
                else:
                    logging.info(f'Успешно куплено {count_purchase} аккаунтов, работа завершена.')
                    return


if __name__ == '__main__':
    config = Config.load_config('config.ini')
    logging.basicConfig(level=config.logging.level, format=config.logging.format)

    main(
        lolzteam_token=config.lolzteam.token, search_url=config.lolzteam.search_url,
        count_accounts=config.lolzteam.count, telegram_token=config.telegram.bot_token,
        telegram_id=config.telegram.id, text=config.telegram.text_message
    )
