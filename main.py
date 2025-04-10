import telebot
import feedparser

# 🔐 Токен (в проде используй переменные окружения)
TOKEN = "7104233246:AAGG94bvzxVog3boMnWWh9wZhczkn5SkfOQ"
bot = telebot.TeleBot(TOKEN)

# 📰 RSS-лента
RSS_URL = "https://habr.com/ru/rss/hubs/python/articles/?fl=ru"

def get_latest_articles(limit=5):
    feed = feedparser.parse(RSS_URL)
    articles = []

    for entry in feed.entries[:limit]:
        title = entry.title
        link = entry.link
        published = entry.published
        summary = entry.summary if hasattr(entry, "summary") else ""
        articles.append(f"📰 <b>{title}</b>\n📅 {published}\n🔗 {link}")
    return articles

# 💬 Команда /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который показывает последние статьи о Python с Habr.\nНапиши /news чтобы получить свежие материалы.")

# 💬 Команда /news
@bot.message_handler(commands=['news'])
def send_news(message):
    bot.send_message(message.chat.id, "Получаю последние статьи...")
    articles = get_latest_articles()
    for article in articles:
        bot.send_message(message.chat.id, article, parse_mode="HTML")

# 🔁 Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
