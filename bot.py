import telebot
import instaloader
import yt_dlp
import os
import time
import pickle

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
IG_USERNAME = 'your_instagram_username'
IG_PASSWORD = 'your_instagram_password'

bot = telebot.TeleBot(API_TOKEN)
L = instaloader.Instaloader()

SESSION_FILE = f"{IG_USERNAME}_session.pkl"

def save_session():
    with open(SESSION_FILE, 'wb') as f:
        pickle.dump(L.context.session, f)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'rb') as f:
            L.context.session = pickle.load(f)
        L.context.log("Session loaded")
        return True
    return False

def instagram_login():
    try:
        if load_session():
            # Test session by trying to get profile
            profile = instaloader.Profile.from_username(L.context, IG_USERNAME)
            print(f"Session valid for {profile.username}")
        else:
            L.login(IG_USERNAME, IG_PASSWORD)
            save_session()
            print("Logged in and session saved")
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False

def download_instagram_reel(url):
    try:
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        caption = post.caption if post.caption else ''
        video_url = post.video_url
        filename = f"{shortcode}.mp4"

        # Download video via requests
        import requests
        r = requests.get(video_url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return filename, caption
    except Exception as e:
        print(f"Instagram reel download error: {e}")
        return None, None

def download_tiktok_video(url):
    ydl_opts = {
        'outtmpl': 'tiktok_video.mp4',
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            caption = info_dict.get('description', '')
            return 'tiktok_video.mp4', caption
    except Exception as e:
        print(f"TikTok download error: {e}")
        return None, None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Send me an Instagram Reels or TikTok link, and I'll download it with caption.")

@bot.message_handler(func=lambda m: True)
def handle_link(message):
    url = message.text.strip()
    bot.reply_to(message, "Processing your link, please wait...")

    if 'instagram.com/reel' in url:
        filename, caption = download_instagram_reel(url)
    elif 'tiktok.com' in url:
        filename, caption = download_tiktok_video(url)
    else:
        bot.reply_to(message, "Unsupported URL. Send an Instagram Reels or TikTok link.")
        return

    if filename:
        bot.reply_to(message, f"Downloaded video!\nCaption:\n{caption}\nUploading in 30 seconds to simulate safe repost...")
        time.sleep(30)

        # Placeholder for upload logic
        bot.reply_to(message, "Pretending to upload video to Instagram Reels now... (this part is a stub)")

        # Clean up downloaded video
        if os.path.exists(filename):
            os.remove(filename)
    else:
        bot.reply_to(message, "Failed to download the video.")

if __name__ == '__main__':
    print("Starting Instagram Telegram Repost Bot...")
    if instagram_login():
        bot.polling()
    else:
        print("Instagram login failed. Exiting.")
