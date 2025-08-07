# telegram_bot.py

import requests

# ✅ आपका Bot Token और Chat ID यहाँ जोड़े गए हैं
TELEGRAM_BOT_TOKEN = '8452064311:AAGzJo8-JqpddDqiy7mzB4_Pz9t5xCJ1FmU'
TELEGRAM_CHAT_ID = '8240596669'

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print('Telegram Error:', response.text)
    except Exception as e:
        print('Telegram Exception:', e)
