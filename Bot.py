import requests
from bs4 import BeautifulSoup
import asyncio
from aiogram import Bot, Dispatcher

# === Налаштування ===
BOT_TOKEN = '6953007603:AAEhzpI7VKVJMQBl9YQoNmNId6mSb5Rkmyg'  # Встав сюди свій токен бота
CHAT_ID = '@MaksANDR1694'      # Встав сюди свій Chat ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Зберігаємо попередню кількість квартир
previous_count = None

# === Функція для парсингу сайту ===
def get_apartments_count():
    url = 'https://atlant.build/obekty/zhk-na-petlyury-28/kompleks-28'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    cards = soup.find_all('div', class_='complex__house-card')
    for card in cards:
        number = card.find('div', class_='complex__house-number')
        if number and number.text.strip() == '3':
            info = card.find('p', class_='complex__house-status')
            if info:
                count = int(''.join(filter(str.isdigit, info.text)))
                return count
    return None

# === Функція для перевірки і відправки повідомлення ===
async def check_apartments():
    global previous_count
    try:
        count = get_apartments_count()
        if count is None:
            await bot.send_message(CHAT_ID, "❌ Не вдалося знайти інформацію про 3-й будинок.")
            return

        if previous_count is None:
            previous_count = count
        elif count != previous_count:
            await bot.send_message(
                CHAT_ID,
                f"🏢 Кількість вільних квартир у 3-му будинку змінилася: {count} (було {previous_count})"
            )
            previous_count = count
    except Exception as e:
        await bot.send_message(CHAT_ID, f"⚠️ Помилка при перевірці: {e}")

# === Головний цикл (перевірка щогодини) ===
async def scheduler():
    while True:
        await check_apartments()
        await asyncio.sleep(3600)  # перевірка кожні 60 хвилин

if __name__ == '__main__':
    asyncio.run(scheduler())
