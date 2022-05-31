from sqlite3 import Error
from time import sleep
from splinter import Browser
import os

from configparser import ConfigParser
config = ConfigParser()

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

botfathercode = os.environ['BOTFATHERCODE']
storecode = os.environ['STORECODE']

config.read('config.ini')
with open('config.ini', 'w') as f:
    config.write(f)


def submit_survey(number, comment):
    try:
        browser = Browser('firefox', headless=True)  # defaults to firefox
        browser.visit('http://dunkinrunsonyou.com/')
        # print("Browser is loading Dunkin")
        sleep(1)
        browser.fill('spl_q_inrest_rcpt_code_txt', number)
        browser.find_by_name('forward_main-pager').click()
        # print("Completing survey")

        sleep(1)

        browser.find_by_id("onf_q_inrest_recommend_ltr_11").click()
        browser.find_by_id("onf_q_inrest_recent_experience_osat_5").click()
        browser.fill('spl_q_inrest_score_cmt', comment)
        browser.find_by_id("buttonNext").click()

        sleep(1)

        browser.find_by_id("onf_q_inrest_speed_of_service_osat_5").click()
        browser.find_by_id("onf_q_inrest_appearence_of_the_restraunt_osat_5").click()
        browser.find_by_id("onf_q_inrest_taste_of_food_osat_5").click()
        browser.find_by_id("onf_q_inrest_friendliness_of_staff_osat_5").click()
        browser.find_by_id("onf_q_inrest_order_fulffiled_yn_1").click()
        browser.find_by_id("onf_q_inrest_visit_experience_yn_2").click()
        browser.find_by_id("buttonNext").click()

        sleep(1)

        browser.find_by_id("onf_q_inrest_rcpt_additional_questions_alt_2").click()
        browser.find_by_id("buttonNext").click()
        # print("Survey " + number + " is complete")
        sleep(3)
    except:
        pass


updater = Updater(botfathercode,
                  use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to the Dunkin Donuts Survey Completer bot! Send /help to get started.")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("Use the /addcodes command to submit surveys. For example \n /addcodes 012345678901234567 \n Use the /score command to show the scoreboard.")


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


def add_to_list(update: Update, context: CallbackContext):
    user = update.message.from_user
    print("Conversation started with " + str(user.username) + " " + str(user.id))
    index: int
    for index, line in enumerate(context.args):
        line = line + " "
        sanitized_code = sanitize_code(line)
        if sanitized_code != "":
            submit_survey(str(sanitized_code).strip(), "")
            if not config.has_option('score', str(user.id)):
                config.set('score', str(user.id), str(0))
            userscore = int(config.get('score', str(user.id)))
            userscore +=1
            config.set('score', str(user.id), str(userscore))
            with open('config.ini', 'w') as f:
                config.write(f)
            update.message.reply_text(
                "Success! Code " + sanitized_code + " was completed! \nYour score is now " + str(userscore) + ".")
        else:
            update.message.reply_text(
                "Failed! Survey code may be mistyped.")
            continue
        print("/addcodes command for " + str(user.id) + " is complete.\n")


def parse_list(update: Update, context: CallbackContext):
    with open('list.txt') as f:
        index: int
        for index, line in enumerate(f):
            print("\nIteration number " + str(index +1))
            sanitized_code = sanitize_code(line)
            if sanitized_code != "":
                submit_survey(str(sanitized_code).strip(), "")
                print("Submitted code number " + str(index + 1) + ".")
                update.message.reply_text(
                    "Success! Code " + sanitized_code + " was completed!" % update.message.text)
            else:
                print("Skipped number " + str(index + 1) + ". \n")
                update.message.reply_text(
                    "Failed! Survey code may be mistyped." % update.message.text)
                continue
        print("Reached the end of list.txt!")


def score(update: Update, context: CallbackContext):
    user = update.message.from_user
    print(str(user.id) + " " + str(user.username) + " has requested the scoreboard.")
    for key, value in config.items("score"):
        # print("ID {} has a score of {}".format(key, value))
        update.message.reply_text("ID {} has a score of {}".format(key, value))


def sanitize_code(code):
    if len(code) != 19:
        # print("Survey code should be 18 numbers long, that one was " + str(len(code)) + ". Ignoring")
        code = ""
        return code
    if code[5:10] != str(storecode):
        # print("Survey code doesn't contain " + str(storecode) " in the correct place, instead we found " + code[5:10] + " Ignoring.")
        code = ""
        return code
    return code


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('parse', parse_list))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('addcodes', add_to_list, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('score', score))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    # Filters out unknown commands
    Filters.command, unknown))

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
print("Script has reached the bottom and the updater is polling\n")
