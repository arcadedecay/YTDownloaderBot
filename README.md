# 🎬 YTDownloaderBot

A free and open-source Telegram bot to download YouTube videos and MP3s, made by [Arcade Decay](https://t.me/ArcadeDecay)!

![Bot Banner](https://telegra.ph/file/2b52fcf03c654ef5a4f51.jpg) <!-- Optional image preview -->

---

## ✨ Features

- ✅ Download YouTube videos as **MP4** or **MP3**
- ✅ Choose from available resolutions: **1080p, 720p, 480p, etc.**
- ✅ Free version: up to **200MB** per download
- ✅ Easy-to-use button interface
- ✅ **Channel join required** before usage
- ✅ Error reporting and support contact buttons
- ✅ Donation and support options
- ✅ Auto clean-up and error handling
- ✅ **100% Open Source**

---

## 📢 Channel Requirement

To use the bot, users **must join** the official channel:

👉 [@ArcadeDecay](https://t.me/ArcadeDecay)

If not joined, the bot will block access.

---

## 🔧 Setup & Run Locally

#1. Clone this repo

     git clone https://github.com/arcadedecay/YTDownloaderBot
    cd YTDownloaderBot

#2. Create .env file 

      BOT_TOKEN=your_bot_token_here

#3.  Install requirements 

      pip install -r requirements.txt

Or. manually:

           
      pip install python-telegram-bot yt-dlp python-dotenv

#4 yt-dlp Installation Required

  For Linux (Debian/Kali/Ubuntu)
  
     sudo apt update        
     sudo apt install yt-dl

For Windows:

Download the yt-dlp.exe from the yt-dlp GitHub Releases(https://github.com/yt-dlp/yt-dlp/releases)

Place it in a folder included in your PATH (e.g., C:\\Windows\\System32) or the same folder as your bot.py.

For Android (Termux):

    pkg update
    pkg install yt-dlp
After installing, instruct them to confirm:

    yt-dlp --version

Install ffmpeg

    sudo apt update
    sudo apt install ffmpeg

On Windows:

Download the ffmpeg static build from ffmpeg.org.(https://ffmpeg.org/download.html)

Extract the folder and add its bin subfolder to your PATH.

Verify with:

    ffmpeg -version
    
On Android (Termux):

    pkg install ffmpeg

✅ Verification:
After installing, users should run:

    yt-dlp --version
    ffmpeg -version
    
⚠️ Note: This bot uses yt-dlp via subprocess. You must install yt-dlp on your system before using this bot.

Run the bot 

      python bot.py 

💬 Bot Commands and Workflow
Start Bot
Bot sends welcome message with info, credits, and instructions.

Send YouTube URL
User gets format buttons (MP3 or MP4 in available resolutions).

Choose Format
Bot downloads and sends the file. Shows:

Warning: This is a beta version

Support link

Donation/Ad link

If Not Joined Channel
Bot blocks usage and shows a “Join Channel” button.

🛠 Support & Contact
❌ Error or bug? Report here: @ArcadeDecaysupportadmin_bot

💬 Want to advise or ask something? DM: @ArcadeDecaysupportadmin_bot

💖 Support Development
This bot is hosted on a free server and may be slow sometimes. If you'd like to support future updates:

👉 Click here to support via ads
👉 Premium version coming soon!

🧠 What is yt-dlp?
      yt-dlp is an advanced fork of youtube-dl. It is used to extract and download videos and audio from YouTube and many other platforms.

We use it to:

Get video/audio streams

Choose quality and format

Save and send it back to users

📄 License
This project is licensed under the MIT License.
© 2025 by Arcade Decay

You are free to modify, share, and use this code — but please credit the original author.

GitHub Repo: https://github.com/arcadedecay/YTDownloaderBot






