import os
import telebot
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, TwoFactorRequired
import time

# Config
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Simpan di Railway Variables
IG_USERNAME = os.getenv("IG_USERNAME")        # Username IG lo
IG_PASSWORD = os.getenv("IG_PASSWORD")        # Password IG lo (HATI-HATI!)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
cl = Client()

# Global variable to store OTP
otp = None

# Login ke Instagram
def instagram_login():
    try:
        cl.login(IG_USERNAME, IG_PASSWORD)
        print("[+] Login Instagram berhasil!")
    except TwoFactorRequired:
        print("[-] 2FA diperlukan, menunggu OTP...")
        return False
    except Exception as e:
        print(f"[-] Gagal login IG: {e}")
        return False
    return True

# Handle Telegram input OTP
@bot.message_handler(func=lambda msg: msg.text.isdigit() and len(msg.text) == 6)
def handle_otp(message):
    global otp
    otp = message.text
    bot.reply_to(message, "🔒 Memasukkan OTP ke Instagram...")
    try:
        # Login ulang dengan OTP
        cl.two_factor_login(IG_USERNAME, OTP=otp)
        bot.reply_to(message, "✅ Berhasil login dengan OTP!")
    except Exception as e:
        bot.reply_to(message, f"❌ Gagal login dengan OTP: {e}")

# Handle pesan di Telegram untuk Reels
@bot.message_handler(func=lambda msg: "instagram.com/reel/" in msg.text)
def handle_reels(message):
    try:
        url = message.text
        bot.reply_to(message, "🔍 Sedang mendownload Reels...")
        
        # Mendapatkan media_pk dari URL
        media_pk = cl.media_pk_from_url(url)
        
        # Mendapatkan informasi media, termasuk caption
        media_info = cl.media_info(media_pk)
        
        # Mengambil caption dari media
        caption = media_info.caption_text if media_info.caption_text else "📥 Via Telegram Bot"
        
        # Download Reels
        video_path = cl.video_download(media_pk)
        
        # Upload ke IG
        bot.reply_to(message, "📤 Mengupload ke Instagram...")
        cl.clip_upload(video_path, caption=caption)
        
        # Menghapus file setelah upload
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"[+] File {video_path} berhasil dihapus setelah diupload.")
        
        bot.reply_to(message, "✅ Berhasil di-repost ke IG dan file dihapus!")
    except Exception as e:
        bot.reply_to(message, f"❌ Gagal: {e}")

# Main execution
print("🤖 Memulai login Instagram...")
if not instagram_login():
    print("[*] Menunggu OTP dari pengguna...")
    bot.polling()

# Start the bot
print("🤖 Bot jalan...")
bot.infinity_polling()
