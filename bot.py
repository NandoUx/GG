import os
import telebot
import re
import uuid
from reposter import process_tiktok_link

API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

ACCOUNTS = ["account1", "account2"]  # Replace with your real account cookie names

@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.reply_to(msg, "👋 Send me a TikTok link to repost.")

@bot.message_handler(func=lambda m: re.search(r'(https?://[^\s]+)', m.text))
def handle_link(msg):
    url = re.search(r'(https?://[^\s]+)', msg.text).group(0)
    bot.reply_to(msg, f"📥 Downloading TikTok: {url}")
    
    selected_account = ACCOUNTS[hash(url) % len(ACCOUNTS)]
    temp_name = f"video_{uuid.uuid4().hex[:6]}.mp4"

    success, caption = process_tiktok_link(url, temp_name, selected_account)
    
    if success:
        bot.reply_to(msg, f"✅ Reposted from {selected_account}\n🧹 Cleaning up...")
    else:
        bot.reply_to(msg, "❌ Failed to repost. Maybe TikTok changed something.")

bot.polling()
