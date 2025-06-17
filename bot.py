"""
YT Downloader Bot - Telegram Bot to download YouTube videos/audio

Created by Arcade Decay
Channel: https://t.me/ArcadeDecay

This code is open source and free to use under the MIT License.
Source code: https://github.com/arcadedecay/YTDownloaderBot

Please support the channel if you find it useful!
"""

import os
import yt_dlp
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "ArcadeDecay"
SUPPORT_BOT = "https://t.me/ArcadeDecaysupportadmin_bot"
ADS_URL = "https://ouo.io/NQQ4OQY"
GITHUB_URL = "https://github.com/arcadedecay/YTDownloaderBot"
DOWNLOAD_LIMIT_MB = 200

async def check_user_joined_channel(app, user_id):
    try:
        member = await app.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    joined = await check_user_joined_channel(context.application, user.id)

    if not joined:
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")]
        ]
        await update.message.reply_text("❌ You must join our channel first!", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    keyboard = [
        [InlineKeyboardButton("🔗 GitHub Source", url=GITHUB_URL)],
        [InlineKeyboardButton("📞 Contact Support", url=SUPPORT_BOT)],
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")]
    ]
    welcome_text = (
        "👋 **Welcome to YTDownloaderBot!**\n\n"
        "🛠️ Made by [Arcade Decay](https://t.me/ArcadeDecay)\n"
        "💻 This bot is open source and free to use.\n\n"
        "🎬 Send a YouTube link below to download MP3 or video up to 200MB.\n\n"
        "**Note**: You must stay in our channel to use this bot.\n\n"
        "❤️ Enjoy the bot? Support us via the ad link below."
    )
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def download_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    joined = await check_user_joined_channel(context.application, user.id)

    if not joined:
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")]
        ]
        await update.message.reply_text("❌ You must join our channel first!", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    url = update.message.text
    context.user_data["url"] = url
    keyboard = [
        [InlineKeyboardButton("🎧 MP3", callback_data="mp3")],
        [InlineKeyboardButton("📹 MP4", callback_data="mp4")]
    ]
    await update.message.reply_text("🔽 Choose download format:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    format_choice = query.data
    url = context.user_data.get("url")
    chat_id = query.message.chat_id

    if not url:
        await query.edit_message_text("⚠️ No video URL found.")
        return

    await query.edit_message_text("⏳ Downloading, please wait...")

    try:
        ydl_opts = {
            "outtmpl": "download.%(ext)s",
            "format": "bestaudio/best" if format_choice == "mp3" else "bestvideo+bestaudio/best",
            "merge_output_format": "mp4" if format_choice == "mp4" else None,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }] if format_choice == "mp3" else []
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            if format_choice == "mp3":
                file_path = os.path.splitext(file_path)[0] + ".mp3"
            else:
                if not file_path.endswith(".mp4"):
                    file_path = os.path.splitext(file_path)[0] + ".mp4"

        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > DOWNLOAD_LIMIT_MB:
            os.remove(file_path)
            await context.bot.send_message(chat_id, f"⚠️ File is {size_mb:.2f}MB — exceeds 200MB free limit.")
            return

        caption = (
            "✅ Your file is ready!\n\n"
            "⚠️ *This bot is in beta — it may have bugs or downtime.*\n"
            f"👉 Want to support? [Click here]({ADS_URL})\n"
            f"📞 Need help? [Contact here]({SUPPORT_BOT})"
        )

        if format_choice == "mp3":
            await context.bot.send_audio(chat_id=chat_id, audio=InputFile(file_path), caption=caption, parse_mode="Markdown")
        else:
            await context.bot.send_video(chat_id=chat_id, video=InputFile(file_path), caption=caption, parse_mode="Markdown")

        os.remove(file_path)

    except Exception as e:
        await context.bot.send_message(chat_id, f"❌ Error: `{e}`", parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_request))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("✅ Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
