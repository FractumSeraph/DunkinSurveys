from sqlite3 import Error
from time import sleep
from splinter import Browser

import os

import sqlite3

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

botfathercode = os.environ['BOTFATHERCODE']

try:
    conn = sqlite3.connect('database.db')
except Error as e:
    print(e)

# Create a cursor to allow to execute SQL commands
# cursor = conn.cursor()

# Create a SQL Table
sql_command = '''
        CREATE TABLE IF NOT EXISTS surveys (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, 
            code TEXT, 
            completed BOOL, 
        )'''


# cursor.execute(sql_command)

# Commit the changes to the database
# conn.commit()


def submit_survey(number, comment):
    try:
        browser = Browser('firefox', headless=True)  # defaults to firefox
        browser.visit('http://dunkinrunsonyou.com/')
        print("Browser is loading Dunkin")
        sleep(1)
        browser.fill('spl_q_inrest_rcpt_code_txt', number)
        browser.find_by_name('forward_main-pager').click()
        print("Completing survey")

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
        print("Survey " + number + " is complete")
        sleep(1)
    except:
        pass


updater = Updater(botfathercode,
                  use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to the Dunkin Donuts Survey Completer bot! Send /help to get started.")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("This bot is still under construction. Commands are disabled.")


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


def add_to_list(update: Update, context: CallbackContext):
    print(len(context.args))
    index: int
    for index, line in enumerate(context.args):
        if len(line) == 18:
            submit_survey(str(line).strip(), "")
            print("Submitted " + str(index + 1) + " surveys.")
        else:
            print("Survey code should be 18 numbers long, that one was " +
                  str(len(line) - 1) + ".")


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
        print("Reached the end of the list!")


def sanitize_code(code):
    if len(code) != 19:
        print("Survey code should be 18 numbers long, that one was " + str(
            len(code)) + ". Ignoring")
        code = ""
        return code
    if code[5:10] != "50180":
        print("Survey code doesn't contain 50180 in the correct place, instead we found " + code[5:10] + " Ignoring.")
        code = ""
        return code
    return code


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('parse', parse_list))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('addcodes', add_to_list, pass_args=True))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    # Filters out unknown commands
    Filters.command, unknown))

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()

print("Script has reached the bottom.")
