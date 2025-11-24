import os
import random
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update
import google.generativeai as genai

# ENV Config
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Gemini Setup
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Funny lines list
funny_lines = [
    "Arey bhai shant ho jaa, battery low lag rhi teri 😭😂",
    "Tu sahi bolta hai... bas koi maanta nahi 😆",
    "Ajeeb insaan ho yaar tum, par cute ho 😹💕",
    "Mat bolo itna, dil pighal jayega mera 🥹😂",
    "Arre arre ruko, CPU garam ho gaya 🤖🔥",
    "Bhai full tatti logic hai tera 😂💩",
    "Oh hello, attitude kam rakho... main bot hoon, bhagwan nahi 😎",
]

# Function to decide mode (funny / AI)
def is_funny(text):
    bad_words = ["bc","mc","gaandu","madarchod","bhosdi","lund","fuck","chutiya"]
    if any(word in text.lower() for word in bad_words):
        return True
    if len(text) < 10:
        return True
    return False

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    # FUNNY MODE
    if is_funny(msg):
        reply = random.choice(funny_lines)
        await update.message.reply_text(reply)
        return

    # GEMINI SMART MODE
    try:
        response = model.generate_content(msg)
        ai_reply = response.text
    except:
        ai_reply = "❌ Gemini se reply nahi mil paya."

    await update.message.reply_text(ai_reply)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))
    print("Bot Running…")
    app.run_polling()

if __name__ == "__main__":
    main()
