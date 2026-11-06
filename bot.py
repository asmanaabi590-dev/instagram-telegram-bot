import os
import logging
import tempfile
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! لینک عمومی پست یا Reel اینستاگرام رو بفرست تا تلاش کنم ویدئو رو برات دریافت کنم."
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = (update.message.text or "").strip()
    if "instagram.com/" not in url:
        await update.message.reply_text("لطفا یک لینک اینستاگرام بفرست")
        return
    await update.message.reply_text("دارم لینک رو بررسی می‌کنم ...")
    with tempfile.TemporaryDirectory() as tmp:
        opts = {
            "outtmpl": str(Path(tmp) / "video.%(ext)s"),
            "format": "best[ext=mp4]/best",
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filepath = Path(ydl.prepare_filename(info))
                if not filepath.exists():
                    candidates = list(Path(tmp).glob("video.*"))
                    if not candidates:
                        raise FileNotFoundError("Downloaded file not found")
                    filepath = candidates[0]
            if filepath.stat().st_size > 49 * 1024 * 1024:
                await update.message.reply_text("حجم ویدئو برای ارسال مستقیم در تلگرام زیاد است")
                return
            with filepath.open("rb") as video:
                await update.message.reply_video(video=video, caption="ویدئوی دریافت‌شده")
        except Exception:
            logging.exception("Download failed")
            await update.message.reply_text(
                "نتونستم این ویدئو رو دریافت کنم. ممکنه پیج خصوصی باشه، لینک محدود شده باشه یا اینستاگرام دسترسی دانلود رو بسته باشه."
            )

async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is required")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await __import__('asyncio').Event().wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
