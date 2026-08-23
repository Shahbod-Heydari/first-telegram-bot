# packages and classes
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
from dotenv import load_dotenv
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)


# bot token
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


# Reply keyboard layout
reply_keyboard = [
    ["Hello", "Profile"],
    ["Settings"]
]

# Create the reply keyboard
reply_markup_forkeys = ReplyKeyboardMarkup(reply_keyboard)



# Inline keyboard layout
inline_keyboard = [
    [
        InlineKeyboardButton("Hello", callback_data="hello"),
        InlineKeyboardButton("Profile", callback_data="profile")
    ]
]

# Create the inline keyboard
inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard)


# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("are")


# Handle text messages and display keyboards
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "glass":
        await update.message.reply_text(
        "Choose something:",
        reply_markup=inline_keyboard_markup
        )

    elif update.message.text == "normal": 
        await update.message.reply_text(
        "Choose something:",
        reply_markup=reply_markup_forkeys
        )
    else:
        await update.message.reply_text("SALAM")
    
    


# Create the Telegram application
app = Application.builder().token(TOKEN).build()


# Register /start command
app.add_handler(CommandHandler("start", start))


# Register handler for text messages
app.add_handler(MessageHandler(filters.TEXT, message_handler))



# Start the bot
app.run_polling()