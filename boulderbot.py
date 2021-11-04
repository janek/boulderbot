import os
import logging
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bouldergarten import book, check


LOCAL = True
PORT = int(os.environ.get('PORT', 5000))
TOKEN = '2020408861:AAGoHkFiO1P231Ymv6BnMYDfmk006SpzucM'

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
    answer = check()
    if answer:
        update.message.reply_text(answer)

def register_command(update, context):
    logger.info("Registration started")
    # Get user data, put in DB
    r = requests.post("https://sheetdb.io/api/v1/3d1qw3odqb5kl", data={"first_name": "Rick"})
    # TODO: check response

def start_command(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def quote(update, context):
    update.message.reply_text('Adjusted Bukowski quote goes here')

def reply(update, context):
    """Reply to the user's message."""
    if update.message.text == "book":
        answer = book()
        if answer:
            update.message.reply_text(answer)
    elif update.message.text == "check":
        update.message.reply_text("Please hold!")
        answer = check()
        if answer:
            update.message.reply_text(answer)
    else:
        update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    logger.info('Starting bot')
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("register", register_command))
    dp.add_handler(CommandHandler("book", book_command))
    dp.add_handler(CommandHandler("check", check_command))

    # on noncommand i.e message - reply the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, quote))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url="https://ricchardo-bukowski.herokuapp.com/" + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    logger.info('Started bot')

if __name__ == '__main__':
    main()
