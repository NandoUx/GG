import telebot
import asyncio
from playwright.async_api import async_playwright

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Send me a TikTok link to repost.")

@bot.message_handler(func=lambda message: 'tiktok.com' in message.text)
def handle_tiktok_link(message):
    url = message.text.strip()
    bot.reply_to(message, "Processing the TikTok link...")
    asyncio.run(process_and_repost(url, message.chat.id))

async def process_and_repost(url, chat_id):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto(url)
        await page.wait_for_timeout(3000)
        
        # Try extract caption
        try:
            caption = await page.inner_text('div[data-e2e="browse-video-desc"]')
        except:
            caption = "No caption found"

        await bot.send_message(chat_id, f"Caption fetched:\n\n{caption}")
        
        # Optional: simulate repost login and upload (not shown here)
        await browser.close()

bot.polling()
