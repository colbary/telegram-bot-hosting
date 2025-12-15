import telebot
from telebot import types
import os
import json
from datetime import datetime
import time
from flask import Flask, request
import threading

# === НАСТРОЙКИ ===
TOKEN = "8253715617:AAG6CyXy55SRB3QZuKqxBaQBm2mfyptuJXw"  # Твой текущий токен
CREATOR = "@ALKOZON"
ADMIN_ID = 8253715617  # Твой ID

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# === ХРАНИЛИЩЕ В ОПЕРАТИВКЕ ===
users_data = {}
codes_sent = 0

CODES = {
    "vpn": {
        "name": "🎮 V2Ray VPN для игр",
        "code": """{
  "inbounds": [{
    "port": 10808,
    "protocol": "socks",
    "settings": {"auth": "noauth", "udp": true}
  }],
  "outbounds": [{
    "protocol": "vmess",
    "settings": {
      "vnext": [{
        "address": "speed.cloudflare.com",
        "port": 443,
        "users": [{
          "id": "b831381d-6324-4d53-ad4f-8cda48b30811",
          "alterId": 0
        }]
      }]
    },
    "streamSettings": {
      "network": "ws",
      "security": "tls",
      "wsSettings": {"path": "/ws"},
      "tlsSettings": {"serverName": "speed.cloudflare.com"}
    }
  }]
}""",
        "instructions": "📋 Инструкция:\n1. Установи V2Ray\n2. Сохрани конфиг как config.json\n3. Запусти: v2ray run -config config.json"
    },
    
    "python": {
        "name": "🐍 Python скрипт",
        "code": """#!/usr/bin/env python3
# Created by @ALKOZON

print("Код от создателя: @ALKOZON")
# Ваш код здесь""",
        "instructions": "💻 Использование:\n1. Сохрани как script.py\n2. Запусти: python script.py"
    }
}

def create_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📤 Publish", "📊 Subscriptions")
    markup.add("⚙️ Edit buttons")
    markup.add("❌ Disconnect", "🔙 Back")
    return markup

def create_code_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🎮 VPN Config", "🐍 Python Code")
    markup.add("📚 All Codes", "👑 Creator")
    markup.add("📊 Statistics", "🔙 Back")
    return markup

# === ОБРАБОТЧИКИ КОМАНД ===
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user = message.from_user
    user_id = user.id
    
    if user_id not in users_data:
        users_data[user_id] = {
            'username': user.username,
            'first_name': user.first_name,
            'join_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'requests': 0
        }
    
    welcome_text = f"""👋 Привет, {user.first_name}!

🤖 <b>Бот работает на GitHub сервере</b>
🎯 <b>Создатель:</b> {CREATOR}
⚡ <b>Статус:</b> Онлайн 24/7

📁 <b>Используй кнопки ниже:</b>"""
    
    bot.send_message(message.chat.id, welcome_text, 
                    parse_mode='HTML',
                    reply_markup=create_main_keyboard())

@bot.message_handler(func=lambda m: m.text == "📤 Publish")
def publish_handler(message):
    bot.send_message(message.chat.id, 
                    "📦 <b>Выберите тип кода:</b>",
                    parse_mode='HTML',
                    reply_markup=create_code_keyboard())

@bot.message_handler(func=lambda m: m.text == "🎮 VPN Config")
def vpn_handler(message):
    global codes_sent
    codes_sent += 1
    
    bot.send_message(message.chat.id,
                    f"📦 <b>VPN Config от {CREATOR}</b>",
                    parse_mode='HTML')
    
    time.sleep(0.3)
    bot.send_message(message.chat.id,
                    f"<code>{CODES['vpn']['code']}</code>",
                    parse_mode='HTML')
    
    time.sleep(0.3)
    bot.send_message(message.chat.id,
                    CODES['vpn']['instructions'],
                    reply_markup=create_code_keyboard())

@bot.message_handler(func=lambda m: m.text == "🐍 Python Code")
def python_handler(message):
    global codes_sent
    codes_sent += 1
    
    bot.send_message(message.chat.id,
                    f"📦 <b>Python Code от {CREATOR}</b>",
                    parse_mode='HTML')
    
    time.sleep(0.3)
    bot.send_message(message.chat.id,
                    f"<code>{CODES['python']['code']}</code>",
                    parse_mode='HTML')
    
    time.sleep(0.3)
    bot.send_message(message.chat.id,
                    CODES['python']['instructions'],
                    reply_markup=create_code_keyboard())

@bot.message_handler(func=lambda m: m.text == "📊 Statistics")
def stats_handler(message):
    stats_text = f"""📊 <b>Статистика сервера:</b>

👥 Пользователей онлайн: {len(users_data)}
📨 Кодов отправлено: {codes_sent}
⚡ Сервер: GitHub Codespaces
🕒 Время: {datetime.now().strftime('%H:%M:%S')}
🎯 Создатель: {CREATOR}

<b>Бот работает 24/7 бесплатно!</b>"""
    
    bot.send_message(message.chat.id, stats_text,
                    parse_mode='HTML',
                    reply_markup=create_code_keyboard())

@bot.message_handler(func=lambda m: m.text == "👑 Creator")
def creator_handler(message):
    bot.send_message(message.chat.id,
                    f"🎯 <b>Создатель:</b> {CREATOR}\n\n"
                    "Все коды собраны специально для вас!\n"
                    "Сервер: GitHub (бесплатный хостинг)",
                    parse_mode='HTML',
                    reply_markup=create_code_keyboard())

@bot.message_handler(func=lambda m: m.text == "📊 Subscriptions")
def subs_handler(message):
    bot.send_message(message.chat.id,
                    f"📊 <b>GitHub Cloud Hosting</b>\n\n"
                    f"Бот работает на бесплатном сервере\n"
                    f"Лимит: 120 часов/месяц\n"
                    f"Доступно всегда\n"
                    f"Создатель: {CREATOR}",
                    parse_mode='HTML',
                    reply_markup=create_main_keyboard())

# === FLASK СЕРВЕР ДЛЯ PING ===
@app.route('/')
def home():
    return f"Bot is running! Creator: {CREATOR} | Users: {len(users_data)}"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return 'Bad request', 400

# === ЗАПУСК БОТА ===
def run_bot():
    print(f"🤖 Бот запущен! Создатель: {CREATOR}")
    print(f"⚡ Сервер: GitHub Codespaces")
    print(f"🔗 Webhook настроен")
    
    # Устанавливаем вебхук
    bot.remove_webhook()
    time.sleep(1)
    
    # В GitHub Codespaces получаем внешний URL
    try:
        # Это для GitHub Codespaces
        codespace_name = os.environ.get('CODESPACE_NAME', 'local')
        if codespace_name != 'local':
            webhook_url = f"https://{codespace_name}-8080.app.github.dev/webhook"
            bot.set_webhook(url=webhook_url)
            print(f"🌐 Webhook URL: {webhook_url}")
    except:
        # Локальный запуск
        bot.polling(none_stop=True)

# === ДВА ВАРИАНТА ЗАПУСКА ===
if __name__ == "__main__":
    # Вариант 1: Запуск вебхука (для GitHub)
    port = int(os.environ.get('PORT', 8080))
    
    # Запускаем в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Запускаем Flask сервер
    app.run(host='0.0.0.0', port=port, debug=False)