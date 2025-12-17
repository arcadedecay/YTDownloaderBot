'''
ArcadeDecay YouTube Downloader Bot (MP3 Fixed)
✅ Uses yt-dlp subprocess
✅ Outputs files with YouTube title for MP3/MP4 correctly
✅ Converts and saves MP3 when requested
✅ Auto-deletes after 30s
'''

import os
import asyncio
import subprocess
import glob
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "ArcadeDecay"
CHANNEL_LINK = os.getenv("CHANNEL_LINK")
SUPPORT_LINK = os.getenv("SUPPORT_LINK")
SUPPORT_AD_LINK = os.getenv("SUPPORT_AD_LINK")

user_format_preferences = {}

async def check_user_joined_channel(app, user_id):
    try:
        member = await app.bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id)
        print(f"[DEBUG] Member status: {member.status}")
        return member.status in ("member", "administrator", "creator")
    except Exception as e:
        print(f"[Channel Join Check Error] {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    joined = await check_user_joined_channel(context.application, user_id)

    if not joined:
        await update.message.reply_text(
            "🚫 Please join our channel to use this bot:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Join Channel", url=CHANNEL_LINK)],
                [InlineKeyboardButton("Try Again ✅", callback_data="check_join")]
            ])
        )
        return

    await update.message.reply_text(
        "**🎉 Welcome to ArcadeDecay YouTube Bot!**\n\nChoose a format to download:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎵 MP3", callback_data="mp3"),
                InlineKeyboardButton("📹 480p", callback_data="480p"),
                InlineKeyboardButton("📺 720p", callback_data="720p"),
                InlineKeyboardButton("🎬 1080p", callback_data="1080p")
            ],
            [InlineKeyboardButton("❗ Report Error", url=SUPPORT_LINK if SUPPORT_LINK.startswith("http") else f"https://{SUPPORT_LINK}"),
             InlineKeyboardButton("❤️ Support via Ads", url=SUPPORT_AD_LINK)]
        ])
    )

async def format_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    format_choice = query.data
    await query.answer()
    user_format_preferences[user_id] = format_choice
    await query.edit_message_text(f"✅ Format selected: {format_choice}\nNow send the YouTube link to download.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    joined = await check_user_joined_channel(context.application, user_id)
    if not joined:
        await update.message.reply_text("🚫 You must join our channel first:")
        return

    await update.message.reply_text("✅ Received! Downloading now, please wait…")
    asyncio.create_task(handle_download_and_send(chat_id, url, context, user_format_preferences.get(user_id, "720p")))

async def handle_download_and_send(chat_id, url, context, format_choice):
    try:
       cmd = [
    "yt-dlp",
    "--js-runtimes", "node"
]
        if format_choice == "mp3":
            cmd += [
                "-f", "bestaudio/best",
                "--extract-audio",
                "--audio-format", "mp3",
                "-o", "%(title)s.%(ext)s",
                url
            ]
        else:
            format_flag = "bestvideo[height<=720]+bestaudio/best"
            if format_choice == "480p":
                format_flag = "bestvideo[height<=480]+bestaudio/best"
            elif format_choice == "720p":
                format_flag = "bestvideo[height<=720]+bestaudio/best"
            elif format_choice == "1080p":
                format_flag = "bestvideo[height<=1080]+bestaudio/best"
            cmd += [
                "-f", format_flag,
                "--merge-output-format", "mp4",
                "-o", "%(title)s.%(ext)s",
                url
            ]

        process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_output = stderr.decode().strip()
            await context.bot.send_message(chat_id=chat_id, text=f"❌ Download failed:\n{error_output}")
            return

        files = glob.glob("*.mp3") if format_choice == "mp3" else glob.glob("*.mp4")
        if not files:
            await context.bot.send_message(chat_id=chat_id, text="❌ Download failed: File not found.")
            return

        file_path = files[0]

        with open(file_path, 'rb') as f:
            if format_choice == "mp3":
                await context.bot.send_audio(chat_id=chat_id, audio=f, read_timeout=120, write_timeout=120, filename=file_path)
            else:
                await context.bot.send_video(chat_id=chat_id, video=f, read_timeout=120, write_timeout=120, filename=file_path)

        await context.bot.send_message(chat_id=chat_id, text="✅ Sent! This file will auto-delete in 30 seconds.")
        await asyncio.sleep(30)

        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"❌ Download error: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(format_selection))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

app.run_polling()
''
