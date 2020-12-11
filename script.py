from telethon.sync import TelegramClient
from telethon import TelegramClient, events, sync
from datetime import date
import random, json, sys, time, re, datetime
from datetime import date, timedelta, datetime, tzinfo
from datetime import datetime, date
from bs4 import BeautifulSoup
import requests


class TimeLoop(object):
    @staticmethod
    def run(channel: list = None) -> 'function':
        def inner_function(function) -> None:
            while True:
                function()
                time.sleep(86400)

        return inner_function


def get_current_course() -> str:
    DOLLAR_RUB = 'https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei=N9l0XtDXHs716QTcuaXoAg&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

    response = requests.get(DOLLAR_RUB, headers=headers)
    html = BeautifulSoup(response.text, 'html.parser')

    return float(
        html.find_all(
            "span",
            {
                "class": "DFlfde",
                "class": "SwHCTb",
                "data-precision": 2
            }
        )[0].get('data-value')
    )


def search_sum(text: str) -> str:
    try:
        return text.split('Кол-во fovcoin: ')[1].split('\n')[0]
    except Exception as error:
        pass


def search_money(text: str) -> str:
    try:
        text = text.split('Сумма: ')[1].split('\n')[0]

        if 'USD' in text:
            return float(text.replace(' USD', '')) * get_current_course()

        return text.replace(' RUB', '')

    except Exception as error:
        pass


def send_message_to_channel() -> None:
    with open('setting.json', 'r', encoding='utf') as out:
        setting = json.load(out)

        client = TelegramClient(
            'session',
            setting['account']['api_id'],
            setting['account']['api_hash']
        )

    client.start()

    dialog = setting['channel']['name']
    messages = client.get_messages(dialog, limit=None)

    messages = [message for message in messages \
                if message.date.strftime('%m-%d-%Y') == datetime.now().strftime('%m-%d-%Y')]

    fcoins_sum = []
    rub_sum = []

    for message in messages:
        try:
            fcoins_sum.append(float(search_sum(message.message)))
        except:
            pass

        try:
            rub_sum.append(float(search_money(message.message)))
        except:
            pass

    client.send_message('https://t.me/fov24h',
                        f'Сводка за 24 часа:')
    client.send_message('https://t.me/fov24h',
                        f'Кол-во Fcoins: {sum(fcoins_sum)},\nСумма: {sum(rub_sum)}₽')


def main(argc: int, argv: list) -> None:
    @TimeLoop.run(channel=['Payment confirmation'])
    def send_message():
        send_message_to_channel()


if __name__ == "__main__":
    main(len(sys.argv[1:]), sys.argv[1:])
