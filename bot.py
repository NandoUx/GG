import os
import re
import telebot
from dotenv import load_dotenv
from tiktok_downloader import download_tiktok_video, extract_caption
from instagram_bot import InstagramBot

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
IG_USERNAME = os.getenv("INSTAGRAM_USERNAME")
IG_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

bot = telebot.TeleBot(BOT_TOKEN)
ig_bot = InstagramBot(IG_USERNAME, IG_PASSWORD)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Send me a TikTok link to repost as Instagram Reel.")

@bot.message_handler(func=lambda m: re.search(r'(https?://[^\s]+)', m.text))
def handle_tiktok_link(message):
    url = re.search(r'(https?://[^\s]+)', message.text).group(0)
    bot.reply_to(message, f"⏳ Downloading TikTok video...")

    video_path = "temp_video.mp4"
    success = download_tiktok_video(url, video_path)
    if not success:
        bot.reply_to(message, "❌ Failed to download the TikTok video.")
        return

    caption = extract_caption(url) or ""

    bot.reply_to(message, "📤 Uploading to Instagram Reels...")
    login_success = ig_bot.login()
    if not login_success:
        bot.reply_to(message, "❌ Failed to login to Instagram.")
        return

    upload_success = ig_bot.upload_reel(video_path, caption)
    if upload_success:
        bot.reply_to(message, "✅ Successfully reposted as Instagram Reel!")
    else:
        bot.reply_to(message, "❌ Failed to upload video to Instagram.")

    if os.path.exists(video_path):
        os.remove(video_path)

if __name__ == '__main__':
    bot.infinity_polling()
