import logging
import os

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()  # Load variables from .env file

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
quivr_token = os.getenv("QUIVR_TOKEN", "")
quivr_chat_id = os.getenv("QUIVR_CHAT_ID", "")
quivr_brain_id = os.getenv("QUIVR_BRAIN_ID", "")
quivr_url = (
    os.getenv("QUIVR_URL", "https://api.quivr.app")
    + f"/chat/{quivr_chat_id}/question?brain_id={quivr_brain_id}"
)

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + quivr_token,
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm Quiv's bot and can answer any question. Please ask your question.",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = requests.post(
        quivr_url, headers=headers, json={"question": user_message}
    )
    if response.status_code == 200:
        quivr_response = response.json().get(
            "assistant", "Sorry, I couldn't understand that."
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=quivr_response
        )
    else:
        # Log or print the response for debugging
        print(f"Error: {response.status_code}, {response.text}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Sorry, there was an error processing your request. {response.text}",
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(telegram_bot_token).build()

    start_handler = CommandHandler("start", start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    application.run_polling()
