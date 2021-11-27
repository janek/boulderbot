import os
import logging
# import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import bouldergarten
import boulderklub


LOCAL = True
PORT = int(os.environ.get('PORT', 5000))
TOKEN = '2020408861:AAGoHkFiO1P231Ymv6BnMYDfmk006SpzucM'
USER = "rrszynka"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def book_command(update, context):
    update.message.reply_text("Booking, please hold!")
    user = update.effective_user
    answer = book(user)
    if answer:
        logger.info("hi")
        update.message.reply_text(answer)

def check_command(update, context):
    update.message.reply_text("Checking, please hold!")
    bouldergarten_answer = bouldergarten.check()
    boulderklub_answer = boulderklub.check()
    if boulderklub_answer and bouldergarten_answer:
        answer = f"♣️ Boulderklub:\n{boulderklub_answer}\n\n🌱Bouldergarten:\n{bouldergarten_answer}"
        update.message.reply_text(answer)

def register_command(update, context):
    logger.info("Registration started")
    # Get user data, put in DB
    # r = requests.post("https://sheetdb.io/api/v1/3d1qw3odqb5kl", data={"first_name": "Rick"})
    # TODO: check response

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def quote(update, context):
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Error "%s" caused by update "%s"', update, context.error)

def program_is_running_on_heroku() -> bool:
    return ('IS_HEROKU' in os.environ)

def main():
    """Start the bot."""
    logger.info('Starting bot')
    logger.info("Running on heroku" if program_is_running_on_heroku() else "Running locally")
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("register", register_command))
    dp.add_handler(CommandHandler("book", book_command))
    dp.add_handler(CommandHandler("check", check_command))

    # on noncommand i.e message - reply the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, quote))

    # on any error caused by message or command
    dp.add_error_handler(error)

    # Start the Bot
    if program_is_running_on_heroku:
        logger.info("Running locally")
        updater.start_polling()
    else:
        logger.info('Running on Heroku')
        updater.start_webhook(listen="0.0.0.0",
                            port=int(PORT),
                            url_path=TOKEN,
                            webhook_url="https://ricchardo-bukowski.herokuapp.com/" + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()
