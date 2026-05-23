import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

BOT_TOKEN = "8215069956:AAEOV4XA1BlW24oRyJpi7FCS0Zq1Uyx-o_c"
MANAGER_CHAT_ID = 472503405

PROJECT_NAME, TOPIC, SUBSCRIBERS, BUDGET, DEADLINE = range(5)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт! Я бот WWC Agency — маркетингового агентства для крипто-проектів та Telegram-каналів.\n\n"
        "Ми допоможемо знайти якісний трафік, запустити рекламу та масштабувати аудиторію 🚀\n\n"
        "Давай заповнимо коротку заявку і наш менеджер зв'яжеться з тобою найближчим часом!\n\n"
        "Як називається твій проект?"
    )
    return PROJECT_NAME

async def project_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['project_name'] = update.message.text
    await update.message.reply_text("📌 Яка тематика проекту? Про що він?")
    return TOPIC

async def topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['topic'] = update.message.text
    await update.message.reply_text("👥 Скільки підписників тобі потрібно?")
    return SUBSCRIBERS

async def subscribers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['subscribers'] = update.message.text
    await update.message.reply_text("💰 Який твій бюджет?")
    return BUDGET

async def budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['budget'] = update.message.text
    await update.message.reply_text("⏰ Які часові обмеження? Коли потрібен результат?")
    return DEADLINE

async def deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['deadline'] = update.message.text

    user = update.message.from_user
    data = context.user_data

    username = f"@{user.username}" if user.username else "немає username"

    message = (
        f"🔔 *Нова заявка!*\n\n"
        f"👤 Від: {user.full_name} ({username})\n"
        f"🆔 ID: `{user.id}`\n\n"
        f"📋 *Деталі:*\n"
        f"• Проект: {data['project_name']}\n"
        f"• Тематика: {data['topic']}\n"
        f"• Підписники: {data['subscribers']}\n"
        f"• Бюджет: {data['budget']}\n"
        f"• Дедлайн: {data['deadline']}"
    )

    await context.bot.send_message(
        chat_id=MANAGER_CHAT_ID,
        text=message,
        parse_mode='Markdown'
    )

    await update.message.reply_text(
        "✅ Дякуємо за заявку!\n\n"
        "Наш менеджер зв'яжеться з тобою найближчим часом 🤝\n\n"
        "Хочеш залишити ще одну заявку? Напиши /start"
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Заявку скасовано. Напиши /start щоб почати знову.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PROJECT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, project_name)],
            TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, topic)],
            SUBSCRIBERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, subscribers)],
            BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, budget)],
            DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, deadline)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)
    print("Бот запущено ✅")
    app.run_polling()

if __name__ == '__main__':
    main()
