import os
import time
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://catalog.onliner.by/sdapi/catalog.api/search/dram?order=price:asc&volume_dram[from]=4gb"
HOUR = 11
MINUTE = 20


def find_ram():
    data = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}).json()
    for ram in data["products"]:
        if ram["prices"]:
            name = ram["full_name"]
            price = ram["prices"]["price_min"]["amount"]
            link = ram["html_url"]
            return f"Самая дешевая оперативка:\n{name}\nЦена: {price} BYN\n{link}"
    return "Ничего не найдено"


def send(text):
    for attempt in range(30):
        try:
            answer = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text}, timeout=20)
            if answer.json()["ok"]:
                print("Отправлено")
                return
            print("Telegram не принял:", answer.json()["description"])
        except Exception as error:
            print("Нет связи с Telegram:", error)
        time.sleep(60)


print(f"Бот работает, жду {HOUR}:{MINUTE}")

while True:
    now = datetime.now()
    if now.hour == HOUR and now.minute == MINUTE:
        try:
            send(find_ram())
        except Exception as error:
            print("Ошибка:", error)
        time.sleep(60)
    time.sleep(30)
