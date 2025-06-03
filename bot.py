import telebot
import instaloader
import os
from dotenv import load_dotenv
from pathlib import Path

# Setup
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
L = instaloader.Instaloader()

user_states = {}
ENV_FILE = ".env"

def update_env(key, value):
    # Update or append to .env
    lines = []
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            lines = f.readlines()

    with open(ENV_FILE, 'w') as f:
        keys_written = set()
        for line in lines:
            if '=' in line:
                k, v = line.strip().split('=', 1)
                if k == key:
                    f.write(f"{key}={value}\n")
                else:
                    f.write(line)
                keys_written.add(k)
            else:
                f.write(line)
        if key not in keys_written:
            f.write(f"{key}={value}\n")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome. Send your Instagram username:")
    user_states[message.chat.id] = {"step": "username"}

@bot.message_handler(func=lambda message: True)
def handle_input(message):
    state = user_states.get(message.chat.id)

    if state and state["step"] == "username":
        state["username"] = message.text.strip()
        state["step"] = "password"
        bot.send_message(message.chat.id, "Now send your Instagram password:")

    elif state and state["step"] == "password":
        username = state["username"]
        password = message.text.strip()

        update_env("IG_USERNAME", username)
        update_env("IG_PASSWORD", password)

        bot.send_message(message.chat.id, "Trying to log in to Instagram...")

        try:
            L.login(username, password)
            L.save_session_to_file(f"{username}_session")
            bot.send_message(message.chat.id, f"✅ Login success! Session saved as {username}_session.")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Login failed: {e}")
        del user_states[message.chat.id]

    else:
        bot.send_message(message.chat.id, "Use /start to begin.")

if __name__ == "__main__":
    print("Bot running...")
    bot.polling()
