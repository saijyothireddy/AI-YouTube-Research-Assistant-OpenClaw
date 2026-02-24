from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

from app.youtube import fetch_transcript
from app.llm import ask_llm
from app.rag import build_index, retrieve
from app.translator import translate
from app.config import BOT_TOKEN

sessions = {}
languages = {}

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.chat_id
    msg = update.message.text

    if msg.startswith("/lang"):
        languages[user] = msg.split()[1]
        await update.message.reply_text("Language updated")
        return

    if "youtube.com" in msg:

        await update.message.reply_text("Processing video...")

        transcript = fetch_transcript(msg)

        chunks = [transcript[i:i+500]
                  for i in range(0, len(transcript), 500)]

        index, chunks = build_index(chunks)
        sessions[user] = (index, chunks)

        prompt = f"""
Give:
1. 5 Key Points
2. Important timestamps
3. Core takeaway

{transcript[:4000]}
"""

        summary = ask_llm(prompt)

        lang = languages.get(user, "en")
        summary = translate(summary, lang)

        await update.message.reply_text(summary)

    else:

        if user not in sessions:
            await update.message.reply_text(
                "Send YouTube link first")
            return

        index, chunks = sessions[user]
        context_text = retrieve(msg, index, chunks)

        prompt = f"""
Answer using context only.

Context:
{context_text}

Question:{msg}

If missing say:
This topic is not covered in the video.
"""

        ans = ask_llm(prompt)

        lang = languages.get(user, "en")
        ans = translate(ans, lang)

        await update.message.reply_text(ans)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))
app.run_polling()
