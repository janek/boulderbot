import os
import logging
import requests
from dataclasses import dataclass
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import time
from gyms import GymName, gyms, get_gym_information

LOCAL = True
PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
DB_API_URL = "https://sheetdb.io/api/v1/3d1qw3odqb5kl"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def book_command(update, context):
    user = update.effective_user
    answer = bouldergarten.book(user)
    if answer:
        logger.info("Received answer from booking")
        update.message.reply_text(answer)


def check_command(update, context):
    logger.info("Starting checking")
    update.message.reply_text("Checking, please hold!")
    for gym in gyms:
        answer = get_gym_information(gym)
        update.message.reply_text(answer)
    logger.info("Finished checking")

def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    update.message.reply_text(update.message.text)

# Currently disabled, was interfering in standard error processing. Could probably work if reconsidered.
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Error "%s" caused by update "%s"', update, context.error)

def program_is_running_on_heroku() -> bool:
    return ('IS_HEROKU' in os.environ)

GET_USER_INFO = 0 # Denotes at which step in getting user registration info we are

def cache_information_about_slots():
    ans = boulderklub.check()
    with open("index.html", "w") as file:
        file.write(ans)

def post_to_webhook():
    info = {"Janek": "cool", "Heroku" : "also cool", "sunday": "great day"}
    info_json = json.dumps(info, indent=4)
    res = requests.post('https://webhook.site/51beee18-e899-48b2-9d54-1b8120ecedde', data=info_json)
    logger.info("post_to_webhook done, " + str(res))


def main():
    if not TOKEN:
        raise Exception(f"Could not retrieve {TELEGRAM_BOT_TOKEN}")
    updater = Updater(TOKEN, use_context=True)
    logger.info("Starting bot on Heroku" if program_is_running_on_heroku() else "Starting bot locally")

    # Register command handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("book", book_command))
    dp.add_handler(CommandHandler("check", check_command))


    # on noncommand i.e message - reply the message on Telegram. Warning: conflicts with the regstration flow!
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Register user registration/reconfiguration flow
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', prompt_for_user_info), CommandHandler('register', prompt_for_user_info)],
        states={
            GET_USER_INFO: [MessageHandler(Filters.text, prompt_for_user_info), CommandHandler('skip', skip)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(conv_handler)

    # Start the bot
    if program_is_running_on_heroku():
        updater.start_webhook(listen="0.0.0.0",
                            port=int(PORT),
                            url_path=TOKEN,
                            webhook_url="https://ricchardo-bukowski.herokuapp.com/" + TOKEN)
        logger.info('Running with webhooks')
    else:
        updater.start_polling()
        logger.info("Started with polling")

    updater.idle()
    # dp.add_error_handler(error)
    schedule.every(30).seconds.do(post_to_webhook)
    while True:
        schedule.run_pending()
        time.sleep(1)
    post_to_webhook()

@dataclass
class UserInfoPrompt:
    slug: str
    prompt: str
    validation_regex: str = None
    required = False
    value: str = None

first_user_info_prompt = """
Editing your configuration. You can always change it later.\n\n
We need personal information in order to book for you. If you /skip a step, I will fill it with a placeholder. \n\n
You need access to the email you give me, and Urban Sports number, if used, has to be correct. \n\n
What's your email?
"""

user_information_prompts = [
    UserInfoPrompt('email', first_user_info_prompt, None, True), # XXX: this should have labels for some KW args for clarity, but that doesn't work for some reason
    UserInfoPrompt('urban_sports_club_id', "Urban Sports Club ID?: \n(write /skip if you don't have one)"),
    UserInfoPrompt('first_name', "First name?"),
    UserInfoPrompt('last_name', "Last name?"),
]

user_prompts_index = 0

def prompt_for_user_info(update: Update, context: CallbackContext) -> int:
    """Ask for user information"""
    # TODO: read out existing info and allow skip if already good
    global user_information_prompts, user_prompts_index
    telegram_username = str(update.effective_user.id)
    user_information = {"telegram_username" : telegram_username}
    if user_prompts_index > 0:
        # TODO: validate via regex before saving, return to this func if not passing
        user_information_prompts[user_prompts_index - 1].value = update.message.text
    if user_prompts_index == len(user_information_prompts):
        update.message.reply_text("Done!")
        user_prompts_index = 0
        for info_prompt in user_information_prompts:
            user_information[info_prompt.slug] = info_prompt.value
        update_user_information(user_information)
        return ConversationHandler.END
    else:
        update.message.reply_text(user_information_prompts[user_prompts_index].prompt)
        user_prompts_index += 1
        return GET_USER_INFO

def update_user_information(user_information):
    # TODO: error handling
    # TODO: register new user vs update existing
    logger.info(user_information)
    endpoint = "/telegram_username/" + user_information['telegram_username']
    print(endpoint)
    r = requests.put(DB_API_URL + "/telegram_username/224704481", user_information)
    logger.info("API says: " + r.text)
    return

def skip(update: Update, context: CallbackContext) -> int:
    """Skip a user information prompt, fill with a placehoder and ask for the next one"""
    # TODO: save placeholder info, maybe extract "save" func from prompt_f_u_i and skip
    return GET_USER_INFO

def cancel(update: Update, context: CallbackContext) -> int:
    # TODO: do we need this?
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

if __name__ == '__main__':
    main()
