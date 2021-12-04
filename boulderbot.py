import os
import logging
# import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import bouldergarten
import boulderklub
import webclimber
import time


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
    answer = bouldergarten.book(user)
    if answer:
        logger.info("hi")
        update.message.reply_text(answer)

def check_command(update, context):
    logger.info("Starting checking")
    update.message.reply_text("Checking, please hold!")

    start_time = time.time()
    boulderklub_answer = boulderklub.check()
    if boulderklub_answer:
        end_time = time.time()
        update.message.reply_text(f"♣️ Boulderklub ({round(end_time - start_time, 2)}s):\n{boulderklub_answer}")

    start_time = time.time()
    bouldergarten_answer = bouldergarten.check()
    if bouldergarten_answer:
        end_time = time.time()
        update.message.reply_text(f"🌱 Bouldergarten ({round(end_time - start_time, 2)}s):\n{bouldergarten_answer}")

    start_time = time.time()
    kegel_answer = webclimber.check("Der Kegel")
    if kegel_answer:
        end_time = time.time()
        update.message.reply_text(f"🔺 Der Kegel ({round(end_time - start_time, 2)}s):\n{kegel_answer}")

    start_time = time.time()
    suedbloc_answer = webclimber.check("Suedbloc")
    if suedbloc_answer:
        end_time = time.time()
        update.message.reply_text(f"🟢 Suedbloc ({round(end_time - start_time, 2)}s):\n{suedbloc_answer}")

    logger.info("Finished checking")

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

    # # Start the Bot
    # if not program_is_running_on_heroku: # TODO: this condition is broken, debug maybe by printing os.environ
    #     logger.info("Running locally")
    #     updater.start_polling()
    # else:

    logger.info('Running with webhooks')
    updater.start_webhook(listen="0.0.0.0",
                        port=int(PORT),
                        url_path=TOKEN,
                        webhook_url="https://ricchardo-bukowski.herokuapp.com/" + TOKEN)
    logger.info('Started webhook')
    updater.idle()

if __name__ == '__main__':
    main()
