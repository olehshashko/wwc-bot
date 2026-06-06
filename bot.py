import telebot
from telebot import types
import requests
import time

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
        'channel': "🔗 Скинь посилання на свій Telegram канал (наприклад t.me/назва):",
        'thanks': "✅ Дякуємо за заявку!\n\nНаш менеджер зв'яжеться з тобою найближчим часом 🤝\n\nХочеш залишити ще одну заявку? Напиши /start",
        'accepted': "✅ Вашу заявку прийнято в роботу! Менеджер зв'яжеться з вами найближчим часом 🤝",
        'rejected': "❌ На жаль, ми не можемо взяти вашу заявку в роботу на даний момент. Якщо є питання — напишіть нам напряму.",
        'channel_error': "⚠️ Не вдалось знайти канал. Перевір посилання і спробуй ще раз (формат: t.me/назва або @назва):",
        'project': "Проект", 'theme': "Тематика", 'subs': "Підписники", 'budget_label': "Бюджет", 'deadline_label': "Дедлайн",
    },
    'ru': {
        'welcome': "👋 Привет! Я бот WWC Agency — маркетингового агентства для крипто-проектов и Telegram-каналов.\n\nМы поможем найти качественный трафик, запустить рекламу и масштабировать аудиторию 🚀\n\nДавай заполним короткую заявку и наш менеджер свяжется с тобой в ближайшее время!\n\nКак называется твой проект?",
        'topic': "📌 Какая тематика проекта? О чём он?",
        'subscribers': "👥 Сколько подписчиков тебе нужно?",
        'budget': "💰 Какой твой бюджет?",
        'deadline': "⏰ Какие временные ограничения? Когда нужен результат?",
        'channel': "🔗 Скинь ссылку на свой Telegram канал (например t.me/название):",
        'thanks': "✅ Спасибо за заявку!\n\nНаш менеджер свяжется с тобой в ближайшее время 🤝\n\nХочешь оставить ещё одну заявку? Напиши /start",
        'accepted': "✅ Ваша заявка принята в работу! Менеджер свяжется с вами в ближайшее время 🤝",
        'rejected': "❌ К сожалению, мы не можем взять вашу заявку в работу. Если есть вопросы — напишите нам напрямую.",
        'channel_error': "⚠️ Не удалось найти канал. Проверь ссылку и попробуй ещё раз (формат: t.me/название или @название):",
        'project': "Проект", 'theme': "Тематика", 'subs': "Подписчики", 'budget_label': "Бюджет", 'deadline_label': "Дедлайн",
    },
    'en': {
        'welcome': "👋 Hi! I'm the WWC Agency bot — a marketing agency for crypto projects and Telegram channels.\n\nWe help find quality traffic, launch ad campaigns and scale your audience 🚀\n\nLet's fill out a quick application and our manager will contact you soon!\n\nWhat is your project called?",
        'topic': "📌 What is the topic of your project?",
        'subscribers': "👥 How many subscribers do you need?",
        'budget': "💰 What is your budget?",
        'deadline': "⏰ Any time constraints? When do you need results?",
        'channel': "🔗 Send a link to your Telegram channel (e.g. t.me/name):",
        'thanks': "✅ Thank you for your application!\n\nOur manager will contact you soon 🤝\n\nWant to submit another? Type /start",
        'accepted': "✅ Your application has been accepted! Our manager will contact you soon 🤝",
        'rejected': "❌ Unfortunately, we cannot take your application at the moment. Contact us directly if you have questions.",
        'channel_error': "⚠️ Channel not found. Check the link and try again (format: t.me/name or @name):",
        'project': "Project", 'theme': "Topic", 'subs': "Subscribers", 'budget_label': "Budget", 'deadline_label': "Deadline",
    }
}

def get_channel_info(username):
    try:
        username = username.strip().replace('https://', '').replace('http://', '')
        if username.startswith('t.me/'):
            username = username[5:]
        if username.startswith('@'):
            username = username[1:]
        username = username.split('/')[0].strip()

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChat"
        resp = requests.get(url, params={'chat_id': f'@{username}'}, timeout=10)
        data = resp.json()
        if not data.get('ok'):
            return None
        chat = data['result']

        count_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMemberCount"
        count_resp = requests.get(count_url, params={'chat_id': f'@{username}'}, timeout=10)
        count_data = count_resp.json()
        member_count = count_data['result'] if count_data.get('ok') else '—'

        return {
            'title': chat.get('title', '—'),
            'username': username,
            'description': chat.get('description', '—'),
            'members': member_count
        }
    except:
        return None

def send_language_keyboard(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_uk"),
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    )
    bot.send_message(chat_id, "🌍 Виберіть мову / Выберите язык / Choose language:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    bot.clear_step_handler_by_chat_id(message.chat.id)
    send_language_keyboard(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def handle_language(call):
    lang = call.data.split('_')[1]
    user_data[call.message.chat.id] = {'lang': lang}
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, TEXTS[lang]['welcome'])
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, get_project_name)

@bot.callback_query_handler(func=lambda call: call.data.startswith('accept_') or call.data.startswith('reject_'))
def handle_manager_action(call):
    parts = call.data.split('_')
    action = parts[0]
    client_chat_id = int(parts[1])
    lang = parts[2] if len(parts) > 2 else 'ru'
    t = TEXTS.get(lang, TEXTS['ru'])

    if action == 'accept':
        bot.send_message(client_chat_id, t['accepted'])
        new_text = call.message.text + "\n\n✅ *Прийнято в роботу*"
        bot.answer_callback_query(call.id, "✅ Клієнту відправлено підтвердження")
    else:
        bot.send_message(client_chat_id, t['rejected'])
        new_text = call.message.text + "\n\n❌ *Відхилено*"
        bot.answer_callback_query(call.id, "❌ Клієнту відправлено відмову")

    bot.edit_message_text(new_text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')

def get_project_name(message):
    if message.text and message.text.startswith('/'): start(message); return
    user_data[message.chat.id]['project_name'] = message.text
    lang = user_data[message.chat.id]['lang']
    bot.send_message(message.chat.id, TEXTS[lang]['topic'])
    bot.register_next_step_handler(message, get_topic)

def get_topic(message):
    if message.text and message.text.startswith('/'): start(message); return
    user_data[message.chat.id]['topic'] = message.text
    lang = user_data[message.chat.id]['lang']
    bot.send_message(message.chat.id, TEXTS[lang]['subscribers'])
    bot.register_next_step_handler(message, get_subscribers)

def get_subscribers(message):
    if message.text and message.text.startswith('/'): start(message); return
    user_data[message.chat.id]['subscribers'] = message.text
    lang = user_data[message.chat.id]['lang']
    bot.send_message(message.chat.id, TEXTS[lang]['budget'])
    bot.register_next_step_handler(message, get_budget)

def get_budget(message):
    if message.text and message.text.startswith('/'): start(message); return
    user_data[message.chat.id]['budget'] = message.text
    lang = user_data[message.chat.id]['lang']
    bot.send_message(message.chat.id, TEXTS[lang]['deadline'])
    bot.register_next_step_handler(message, get_deadline)

def get_deadline(message):
    if message.text and message.text.startswith('/'): start(message); return
    user_data[message.chat.id]['deadline'] = message.text
    lang = user_data[message.chat.id]['lang']
    bot.send_message(message.chat.id, TEXTS[lang]['channel'])
    bot.register_next_step_handler(message, get_channel)

def get_channel(message):
    if message.text and message.text.startswith('/'): start(message); return
    lang = user_data[message.chat.id]['lang']
    t = TEXTS[lang]

    channel_info = get_channel_info(message.text)

    if not channel_info:
        bot.send_message(message.chat.id, t['channel_error'])
        bot.register_next_step_handler(message, get_channel)
        return

    user_data[message.chat.id]['channel'] = message.text
    user_data[message.chat.id]['channel_info'] = channel_info

    data = user_data[message.chat.id]
    flag = {"uk": "🇺🇦", "ru": "🇷🇺", "en": "🇬🇧"}.get(lang, "")
    username = f"@{message.from_user.username}" if message.from_user.username else "—"

    manager_message = (
        f"🔔 *Нова заявка WWC Agency!*\n\n"
        f"👤 {message.from_user.full_name} ({username})\n"
        f"🆔 `{message.chat.id}`\n"
        f"🌍 {flag}\n\n"
        f"• {t['project']}: {data['project_name']}\n"
        f"• {t['theme']}: {data['topic']}\n"
        f"• {t['subs']}: {data['subscribers']}\n"
        f"• {t['budget_label']}: {data['budget']}\n"
        f"• {t['deadline_label']}: {data['deadline']}\n\n"
        f"📊 *Канал клієнта:*\n"
        f"• Назва: {channel_info['title']}\n"
        f"• @{channel_info['username']}\n"
        f"• Підписників: {channel_info['members']}\n"
        f"• Опис: {channel_info['description'][:100] if channel_info['description'] != '—' else '—'}"
    )

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("✅ Взяти в роботу", callback_data=f"accept_{message.chat.id}_{lang}"),
        types.InlineKeyboardButton("❌ Відхилити", callback_data=f"reject_{message.chat.id}_{lang}")
    )

    bot.send_message(MANAGER_CHAT_ID, manager_message, parse_mode='Markdown', reply_markup=markup)
    bot.send_message(message.chat.id, t['thanks'])

print("Бот запущено ✅")
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Помилка: {e}")
        time.sleep(5)
