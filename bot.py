"""
Telegram YouTube Downloader Bot
Created by ArcadeDecay
Channel: https://t.me/ArcadeDecay
Source Code: https://github.com/ArcadeDecay/telegram-ytdl-bot

This code is open source and free to use under the MIT License.
Please give credit to ArcadeDecay when using or modifying this bot.

Support: t.me/ArcadeDecaysupportadmin_bot
"""

import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "ArcadeDecay"
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/ArcadeDecay")
SUPPORT_LINK = os.getenv("SUPPORT_BOT_LINK", "https://t.me/ArcadeDecaysupportadmin_bot")
GITHUB_LINK = "https://github.com/ArcadeDecay/telegram-ytdl-bot"
ADS_LINK = "https://ouo.io/NQQ4OQY"

# --- Helper to check if user has joined channel ---
async def check_user_joined_channel(app, user_id):
    try:
        member = await app.bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False

# --- Start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    joined = await check_user_joined_channel(context.application, user_id)

    if not joined:
        await update.message.reply_text(
            "🚫 Please join our channel to use this bot:\n👉 https://t.me/ArcadeDecay",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Join Channel", url=CHANNEL_LINK)],
                [InlineKeyboardButton("🔁 Check Again", callback_data="check_join")]
            ])
        )
        return

    await update.message.reply_text(
        "**🎉 Welcome to ArcadeDecay YouTube Downloader Bot!**\n\n"
        "📌 This bot is created by [ArcadeDecay](https://t.me/ArcadeDecay)\n"
        "💡 [Open-source on GitHub]({github})\n"
        "💬 Support or advice: @{support}\n\n"
        "✅ Free usage: Up to 200MB per download\n"
        "🛡️ We do not store your video; it will be auto-deleted after 30 seconds.\n"
        "⚠️ Premium version coming soon!\n\n"
        "Choose a format to download 👇"
        .format(github=GITHUB_LINK, support=SUPPORT_LINK.replace("https://t.me/", "")),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎵 MP3", callback_data="mp3"),
                InlineKeyboardButton("📹 480p", callback_data="480p"),
                InlineKeyboardButton("📺 720p", callback_data="720p"),
                InlineKeyboardButton("🎬 1080p", callback_data="1080p")
            ],
            [InlineKeyboardButton("❗ Report Bug", url=SUPPORT_LINK)],
            [InlineKeyboardButton("📂 GitHub Project", url=GITHUB_LINK)],
            [InlineKeyboardButton("❤️ Support Us via Ads", url=ADS_LINK)]
        ])
    )

# --- Download Handler ---
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    joined = await check_user_joined_channel(context.application, user_id)
    if not joined:
        await update.message.reply_text("🚫 You must join our channel first:\n👉 https://t.me/ArcadeDecay")
        return

    await update.message.reply_text("⏳ Downloading your video...")

    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'bestvideo[height<=720]+bestaudio/best',
            'merge_output_format': 'mp4',
            'max_filesize': 200 * 1024 * 1024,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            if not file_path.endswith('.mp4'):
                file_path = file_path.rsplit('.', 1)[0] + '.mp4'

        await context.bot.send_video(chat_id=chat_id, video=open(file_path, 'rb'))

        await update.message.reply_text(
            "✅ Download complete!\n\n"
            "🕒 This file will be auto-deleted in 30 seconds for privacy.\n"
            "⚠️ This bot is still in beta. Bugs may occur.\n"
            "❤️ [Click here to support via Ads]({ads})\n"
            "🔧 Need help? Contact [Support Bot]({support})"
            .format(ads=ADS_LINK, support=SUPPORT_LINK),
            parse_mode="Markdown"
        )

        # Wait and then delete file
        await asyncio.sleep(30)
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}\n\n📩 Contact: @{SUPPORT_LINK.replace('https://t.me/', '')}")

# --- App Setup ---
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

# --- Start Bot ---
app.run_polling()
