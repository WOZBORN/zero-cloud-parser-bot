import random

import telebot
import feedparser
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔐 Токен (в проде используй переменные окружения)
TOKEN = "7104233246:AAGG94bvzxVog3boMnWWh9wZhczkn5SkfOQ"
bot = telebot.TeleBot(TOKEN)

# 📰 RSS-ссылки
RSS_SOURCES = {
    "python": "https://habr.com/ru/rss/hubs/python/articles/?fl=ru",
    "chatgpt": "https://habr.com/ru/rss/search/?q=chatgpt&order_by=relevance&target_type=posts&hl=ru&fl=ru",
    "vk": "https://habr.com/ru/rss/companies/vk/articles/?fl=ru"
}

def get_latest_articles(rss_url, limit=5):
    feed = feedparser.parse(rss_url)
    articles = []

    for entry in feed.entries[:limit]:
        title = entry.title
        link = entry.link
        published = entry.published
        articles.append(f"📰 <b>{title}</b>\n📅 {published}\n🔗 {link}")
    return articles

# 💬 Команда /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🐍 Python", callback_data="news_python"),
        InlineKeyboardButton("🤖 ChatGPT", callback_data="news_chatgpt"),
        InlineKeyboardButton("💙 VK", callback_data="news_vk")
    )
    if (random.randint(0, 1) == 0):
        url = "https://cdn.mtdv.me/video/rick.mp4"
    else:
        url = "https://habr.com/ru/feed/"
    markup.add(InlineKeyboardButton("📖 Хабр", url=url))
    bot.send_message(
        message.chat.id,
        "Привет! Я бот, который показывает свежие статьи с Habr.\nВыбери тему:",
        reply_markup=markup
    )

# 💬 Команда /news
@bot.message_handler(commands=['news'])
def ask_topic(message):
    try:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🐍 Python", callback_data="news_python"),
            InlineKeyboardButton("🤖 ChatGPT", callback_data="news_chatgpt"),
            InlineKeyboardButton("💙 VK", callback_data="news_vk")
        )
        message_text = "какаой-то текст"
        message_count = len(message_text)//4096
        for i in range(message_count+1):
            bot.send_message(message.chat.id, message_text[i*4096:(i+1)*4096], reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "Произошла непредвиденная ошибка! Можете написать в поддержку @support")
        # Залогировать ошибку

# 🔘 Обработка выбора темы
@bot.callback_query_handler(func=lambda call: call.data.startswith("news_"))
def handle_news_choice(call):
    topic = call.data.split("_")[1]
    rss_url = RSS_SOURCES.get(topic)
    if not rss_url:
        bot.answer_callback_query(call.id, "Источник не найден.")
        return

    bot.answer_callback_query(call.id, f"Загружаю {topic.capitalize()} статьи...")
    articles = get_latest_articles(rss_url)
    for article in articles:
        bot.send_message(call.message.chat.id, article, parse_mode="HTML")

# 🔁 Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_poling()
