# packages and classes
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
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


# Profile inline keyboard layout
profile_keyboard = [
    [
        InlineKeyboardButton("Back", callback_data="back")
    ]
]

# Create the profile inline keyboard
profile_markup = InlineKeyboardMarkup(profile_keyboard)



# /start command handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("you picked start command")

# Handle commands that don't have their own dedicated CommandHandler
async def unknown_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I don't know that command.")



# Handle "glass" messages by sending an inline keyboard
async def glass_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Choose something:",
        reply_markup=inline_keyboard_markup
    )



# Handle "normal" messages by sending a reply keyboard
async def normal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Choose something:",
        reply_markup=reply_markup_forkeys
    )



# Handle other text messages by replying with "SALAM"
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("SALAM")



# Handle inline keyboard button presses
async def inline_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if query.data == "hello":
        await query.message.reply_text("you pressed hello in inline keys")
    elif query.data == "profile":
         await query.edit_message_text("Your profile",reply_markup=profile_markup)
    elif query.data == "back":
        await query.edit_message_text("Choose something:",reply_markup=inline_keyboard_markup)



# Handle messages that contain a photo
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("nice photo!")

    # largest photo
    largest_photo = update.message.photo[-1]

    file_id = largest_photo.file_id

    await update.message.reply_photo(photo=file_id)



# Handle messages that contain a video
async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("cool video!")



# Handle messages that contain a document
async def document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("good document")



# Create the Telegram application
app = Application.builder().token(TOKEN).build()



# Register /start command
app.add_handler(CommandHandler("start", start_command))

# Register a handler for any command
app.add_handler(MessageHandler(filters.COMMAND, unknown_command_handler))



# Register handler for messages that are exactly "glass"
app.add_handler(MessageHandler(filters.Regex("^glass$"), glass_handler))

# Register handler for messages that are exactly "normal"
app.add_handler(MessageHandler(filters.Regex("^normal$"), normal_handler))

# Register handler for other text messages
app.add_handler(MessageHandler(filters.TEXT, message_handler))

# Register handler for inline keyboard button presses
app.add_handler(CallbackQueryHandler(inline_button_handler))



# Register handler for messages that contain a photo
app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

# Register handler for messages that contain a video
app.add_handler(MessageHandler(filters.VIDEO, video_handler))

# Register handler for messages that contain any type of document
app.add_handler(MessageHandler(filters.Document.ALL, document_handler))



# Start the bot
app.run_polling()