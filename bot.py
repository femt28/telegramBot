import os
import telebot
import random
import time

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello', 'hi'])
def send_welcome(message):
    bot.reply_to(message, 'Hello {}!'.format(message.from_user.first_name))


@bot.message_handler(commands=['ChooseForMe'])
def handle_movie(message):
    chat_id = message.chat.id
    msg_string = str(message.text)
    cmd = msg_string.split("\n")
    if cmd[0] == '/start':
        bot.send_message(chat_id, "Send stuff line by line")
    else:
        bot.send_message(chat_id, "Hmm thinking...")
        time.sleep(0.5)
        bot.send_message(chat_id, "...")
        time.sleep(0.5)
        bot.send_message(chat_id, "I choose " + random.choice(cmd[1:]))


bot.infinity_polling()
