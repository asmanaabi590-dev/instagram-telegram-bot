Instagram-to-Telegram bot starter

Files:
- bot.py: bot code
- requirements.txt: Python packages

Important:
1. Create a bot with BotFather.
2. Set the environment variable BOT_TOKEN to the bot token in your hosting provider's private/secrets settings. Never paste the token into chat or commit it to GitHub.
3. Install packages from requirements.txt.
4. Run: python bot.py

The bot responds to /start and attempts to download public Instagram video links using yt-dlp. Instagram may block downloads; private posts and login-restricted content will not work. Only download content you have permission to save. Telegram upload size limits may also prevent delivery.
