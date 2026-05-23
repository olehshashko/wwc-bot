import telebot
from telebot import types

BOT_TOKEN = "8215069956:AAEOV4XA1BlW24oRyJpi7FCS0Zq1Uyx-o_c"
MANAGER_CHAT_ID = 472503405

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    bot.send_message(
        message.chat.id,
        "👋 Привіт! Я бот WWC Agency — маркетингового агентства для крипто-проектів та Telegram-каналів.\n\n"
        "Ми допоможемо знайти якісний трафік, запустити рекламу та масштабувати аудиторію 🚀\n\n"
        "Давай заповнимо коротку заявку і наш менеджер зв'яжеться з тобою найближчим часом!\n\n"
        "Як називається твій проект?"
    )
    bot.register_next_step_handler(message, get_project_name)

def get_project_name(message):
    user_data[message.chat.id]['project_name'] = message.text
    bot.send_message(message.chat.id, "📌 Яка тематика проекту? Про що він?")
    bot.register_next_step_handler(message, get_topic)

def get_topic(message):
    user_data[message.chat.id]['topic'] = message.text
    bot.send_message(message.chat.id, "👥 Скільки підписників тобі потрібно?")
    bot.register_next_step_handler(message, get_subscribers)

def get_subscribers(message):
    user_data[message.chat.id]['subscribers'] = message.text
    bot.send_message(message.chat.id, "💰 Який твій бюджет?")
    bot.register_next_step_handler(message, get_budget)

def get_budget(message):
    user_data[message.chat.id]['budget'] = message.text
    bot.send_message(message.chat.id, "⏰ Які часові обмеження? Коли потрібен результат?")
    bot.register_next_step_handler(message, get_deadline)

def get_deadline(message):
    user_data[message.chat.id]['deadline'] = message.text
    data = user_data[message.chat.id]

    username = f"@{message.from_user.username}" if message.from_user.username else "немає username"

    manager_message = (
        f"🔔 *Нова заявка!*\n\n"
        f"👤 Від: {message.from_user.full_name} ({username})\n"
        f"🆔 ID: `{message.chat.id}`\n\n"
        f"📋 *Деталі:*\n"
        f"• Проект: {data['project_name']}\n"
        f"• Тематика: {data['topic']}\n"
        f"• Підписники: {data['subscribers']}\n"
        f"• Бюджет: {data['budget']}\n"
        f"• Дедлайн: {data['deadline']}"
    )

    bot.send_message(MANAGER_CHAT_ID, manager_message, parse_mode='Markdown')

    bot.send_message(
        message.chat.id,
        "✅ Дякуємо за заявку!\n\n"
        "Наш менеджер зв'яжеться з тобою найближчим часом 🤝\n\n"
        "Хочеш залишити ще одну заявку? Напиши /start"
    )

print("Бот запущено ✅")
bot.infinity_polling()
