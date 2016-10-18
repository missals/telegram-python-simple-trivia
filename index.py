#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import (ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
from random import randint
import sqlite3 as lite
import sys
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

Q1, Q2, CHECKANSWER, SOAL3, LOCATION, BIO = range(6)

def totalrow():
    con = lite.connect('test.db')
    with con:
        cur = con.cursor()
        result = cur.execute('SELECT COUNT(*) FROM questions').fetchone()[0]
    con.close()
    return result

def random():
    return randint(0,totalrow())

def getsoal(nomor):
    con = lite.connect('test.db')
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM questions WHERE id=?', nomor)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            soalrow = row
    con.close()
    return soalrow

def start(bot, update):
    reply_keyboard = [['Start !!']]

    update.message.reply_text(
        'Hi! '
        'Choose the correct answer from the following questions.\n\n'
        'Ready ? Click the Start Button Below !',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return Q1

def createquestion():
    question = getsoal(str(random()))
    return question

def q1(bot, update):
    question = createquestion()
    # question[0] == id of the question from database
    # question[1] == the question text
    # question[2] == the A option text
    # question[3] == the B option text
    # question[4] == the C option text
    # question[5] == the D option text
    # question[6] == the E option text
    # question[7] == the Answer Option (in A, B, C, D or E)
    # question[8] == the Reason behind the answer
    reply_keyboard = [['A', 'B'], ['C', 'D'], ['E']]

    update.message.reply_text(
         question[1] + '\n'
         'A ' + question[2] + ' :\n'
         'B ' + question[3] + '\n'
         'C ' + question[4] + '\n'
         'D ' + question[5] + '\n'
         'E ' + question[6] + '\n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CHECKANSWER, question   


def check(bot, update, question):

    if update.message.text == question[7]:
        update.message.reply_text('Correct ! \n' + 'Reason: \n' + question[8])
    else:
        update.message.reply_text('Wrong ! \n' + 'The Answer is ' + question[7] + '\n' + 'Reason: \n' + question[8])
    return Q1


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("231691134:AAF14hNX0XqhwFkzXH76B-BS18fJPxGsfWo")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            Q1: [RegexHandler('^(MULAI !!)$', q1)],
            CHECKANSWER: [RegexHandler('^(A|B|C|D|E)$', check)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    #dp.add_handler(MessageHandler([Filters.text], cekjawaban))

    dp.add_handler(conv_handler)
    #dp.add_handler(MessageHandler([Filters.text], cekjawaban))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()