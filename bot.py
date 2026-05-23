import telebot
from telebot import types

BOT_TOKEN = "8215069956:AAEOV4XA1BlW24oRyJpi7FCS0Zq1Uyx-o_c"
MANAGER_CHAT_ID = 472503405

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

TEXTS = {
    'uk': {
        'welcome': "👋 Привіт! Я бот WWC Agency — маркетингового агентства для крипто-проектів та Telegram-каналів.\n\nМи допоможемо знайти якісний трафік, запустити рекламу та масштабувати аудиторію 🚀\n\nДавай заповнимо коротку заявку і наш менеджер зв'яжеться з тобою найближчим часом!\n\nЯк називається твій проект?",
        'topic': "📌 Яка тематика проекту? Про що він?",
        'subscribers': "👥 Скільки підписників тобі потрібно?",
        'budget': "💰 Який твій бюджет?",
        'deadline': "⏰ Які часові обмеження? Коли потрібен результат?",
        'thanks': "✅ Дякуємо за заявку!\n\nНаш менеджер зв'яжеться з тобою найближчим часом 🤝\n\nХочеш залишити ще одну заявку? Напиши /start",
        'new_app': "🔔 *Нова заявка!*",
        'project': "Проект",
        'theme': "Тематика",
        'subs': "Підписники",
        'budget_label': "Бюджет",
        'deadline_label': "Дедлайн",
        'lang': "🇺🇦 Українська",
    },
    'ru': {
        'welcome': "👋 Привет! Я бот WWC Agency — маркетингового агентства для крипто-проектов и Telegram-каналов.\n\nМы поможем найти качественный трафик, запустить рекламу и масштабировать аудиторию 🚀\n\nДавай заполним короткую заявку и наш менеджер свяжется с тобой в ближайшее время!\n\nКак называется твой проект?",
        'topic': "📌 Какая тематика проекта? О чём он?",
        'subscribers': "👥 Сколько подписчиков тебе нужно?",
        'budget': "💰 Какой твой бюджет?",
        'deadline': "⏰ Какие временные ограничения? Когда нужен результат?",
        'thanks': "✅ Спасибо за заявку!\n\nНаш менеджер свяжется с тобой в ближайшее время 🤝\n\nХочешь оставить ещё одну заявку? Напиши /start",
        'new_app': "🔔 *Новая заявка!*",
        'project': "Проект",
        'theme': "Тематика",
        'subs': "Подписчики",
        'budget_label': "Бюджет",
        'deadline_label': "Дедлайн",
        'lang': "🇷🇺 Русский",
    },
    'en': {
        'welcome': "👋 Hi! I'm the WWC Agency bot — a marketing agency for crypto projects and Telegram channels.\n\nWe help find quality traffic, launch ad campaigns and scale your audience 🚀\n\nLet's fill out a quick application and our manager will contact you soon!\n\nWhat is your project called?",
        'topic': "📌 What is the topic of your project? What is it about?",
        'subscribers': "👥 How many subscribers do you need?",
        'budget': "💰 What is your budget?",
        'deadline': "⏰ Any time constraints? When do you need results?",
        'thanks': "✅ Thank you for your application!\n\nOur manager will contact you soon 🤝\n\nWant to submit another application? Type /start",
        'new_app': "🔔 *New application!*",
        'project': "Project",
        'theme': "Topic",
        'subs': "Subscribers",
        'budget_label': "Budget",
        'deadline_label': "Deadline",
        'lang': "🇬🇧 English",
    }
}

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🇺🇦 Українська", "🇷🇺 Русский", "🇬🇧 English")
    bot.send_message(message.chat.id, "🌍 Виберіть мову / Выберите язык / Choose language:", reply_markup=markup)
    bot.register_next_step_handler(message, get_language)

def get_language(message):
    lang_map = {
        "🇺🇦 Українська": "uk",
        "🇷🇺 Русский": "ru",
        "🇬🇧 English": "en"
    }
    lang = lang_map.get(message.text, "uk")
    user_data[message.chat.id]['lang'] = lang
    t = TEXTS[lang]
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, t['welcome'], reply_markup=markup)
    bot.register_next_step_handler(message, get_project_name)

def get_project_name(message):
    user_data[message.chat.id]['project_name'] = message.text
    lang = user_data[message.chat.id]['lang']
    bot.send_message(message.chat.id, TEXTS[lang]['topic'])
    bot.register_next_step_handler(message, get_topic)

def get_topic(message):
    user_data[message.chat.id]['topic'] = message.text
    lang = user_data[message.chat.id]['lang']
    bot.send_message(message.chat.id, TEXTS[lang]['subscribers'])
    bot.register_next_step_handler(message, get_subscribers)

def get_subscribers(message):
    user_data[message.chat.id]['subscribers'] = message.text
    lang = user_data[message.chat.id]['lang']
    bot.send_message(message.chat.id, TEXTS[lang]['budget'])
    bot.register_next_step_handler(message, get_budget)

def get_budget(message):
    user_data[message.chat.id]['budget'] = message.text
    lang = user_data[message.chat.id]['lang']
    bot.send_message(message.chat.id, TEXTS[lang]['deadline'])
    bot.register_next_step_handler(message, get_deadline)

def get_deadline(message):
    user_data[message.chat.id]['deadline'] = message.text
    data = user_data[message.chat.id]
    lang = data['lang']
    t = TEXTS[lang]

    username = f"@{message.from_user.username}" if message.from_user.username else "—"
    flag = {"uk": "🇺🇦", "ru": "🇷🇺", "en": "🇬🇧"}.get(lang, "")

    manager_message = (
        f"{t['new_app']}\n\n"
        f"👤 {message.from_user.full_name} ({username})\n"
        f"🆔 `{message.chat.id}`\n"
        f"🌍 {flag}\n\n"
        f"📋 *Деталі:*\n"
        f"• {t['project']}: {data['project_name']}\n"
        f"• {t['theme']}: {data['topic']}\n"
        f"• {t['subs']}: {data['subscribers']}\n"
        f"• {t['budget_label']}: {data['budget']}\n"
        f"• {t['deadline_label']}: {data['deadline']}"
    )

    bot.send_message(MANAGER_CHAT_ID, manager_message, parse_mode='Markdown')
    bot.send_message(message.chat.id, t['thanks'])

print("Бот запущено ✅")
bot.infinity_polling()
