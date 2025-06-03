import os
import telebot
import re

API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# Respond to /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Send me a TikTok link and I'll repost it (soon™).")

# Detect TikTok links in messages
@bot.message_handler(func=lambda m: re.search(r'(https?://)?(www\.)?tiktok\.com/', m.text))
def handle_tiktok_link(message):
    tiktok_url = re.search(r'(https?://[^\s]+)', message.text)
    if tiktok_url:
        bot.reply_to(message, f"📥 Got it! Preparing to repost: {tiktok_url.group(0)}")
        # Here you would put your repost logic — right now it's just confirming it works.
    else:
        bot.reply_to(message, "Hmm... that doesn't look like a valid TikTok URL.")

bot.polling()
