import os
import telebot
from instagrapi import Client
from instagrapi.exceptions import LoginRequired


# Config
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Simpan di Railway Variables
IG_USERNAME = os.getenv("IG_USERNAME")        # Username IG lo
IG_PASSWORD = os.getenv("IG_PASSWORD")        # Password IG lo (HATI-HATI!)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
cl = Client()

# Login ke Instagram
try:
    cl.login(IG_USERNAME, IG_PASSWORD)
    print("[+] Login Instagram berhasil!")
except Exception as e:
    print(f"[-] Gagal login IG: {e}")

# Handle pesan di Telegram
@bot.message_handler(func=lambda msg: "instagram.com/reel/" in msg.text)
def handle_reels(message):
    try:
        url = message.text
        bot.reply_to(message, "🔍 Sedang mendownload Reels...")
        
        # Download Reels
        video_path = cl.video_download(cl.media_pk_from_url(url))
        
        # Upload ke IG
        bot.reply_to(message, "📤 Mengupload ke Instagram...")
        cl.clip_upload(video_path, caption="📥 Via Telegram Bot")
        
        bot.reply_to(message, "✅ Berhasil di-repost ke IG!")
    except Exception as e:
        bot.reply_to(message, f"❌ Gagal: {e}")

print("🤖 Bot jalan...")
bot.infinity_polling()
