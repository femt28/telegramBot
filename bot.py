import os
import telebot
import random
import time
import urllib.parse
import requests
import json

BOT_TOKEN = os.environ.get('BOT_TOKEN')
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)

# commands in string for start and help display
COMMANDS = [
    "/start - Start the bot",
    "/help - Show this message",
    "/choose - Let the bot choose from a list of movies",
    "/search - search the web for a movie"
]

# commands in BotCommand Type for set commands
COMMANDS_DICT = [telebot.types.BotCommand("/start", "Start the bot"),
                 telebot.types.BotCommand("/help", "Show this message"),
                 telebot.types.BotCommand("/choose", "Let the bot choose from a list of movies"),
                 telebot.types.BotCommand("/search", "search the web for a movie")
                 ]

bot.set_my_commands(COMMANDS_DICT)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hello {}!'.format(message.from_user.first_name))
    send_help(message)  # sends command list


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "Here are the available commands:\n" + "\n".join(COMMANDS)
    bot.reply_to(message, help_text)


@bot.message_handler(commands=['choose'])
def handle_movie(message):
    chat_id = message.chat.id
    msg_string = str(message.text)
    cmd = msg_string.split("\n")  # split message into array

    # bot actions
    bot.send_message(chat_id, "Hmm thinking...")
    time.sleep(0.5)
    bot.send_message(chat_id, "...")
    time.sleep(0.5)
    try:
        chosen = random.choice(cmd[1:])
        bot.send_message(chat_id, "I choose " + chosen)
        bot.send_message(chat_id, f"Search up this movie with /search {chosen}")
        bot.send_message(chat_id, f"/search {chosen}")
    except IndexError:  # empty list
        bot.send_message(chat_id, "There is nothing to choose")
        bot.send_message(chat_id, "Send /choose with a list of movies underneath")
    finally:
        bot.send_message(chat_id, "Hope this helped :)")


@bot.message_handler(commands=['search'])
def handle_search(message):
    chat_id = message.chat.id

    query = message.text[len('/search '):].strip()

    if not query:
        bot.reply_to(message, "Please enter a movie title")
        return

    # Google search
    search_url = "https://www.google.com/search?q=" + urllib.parse.quote(query + " movie")
    response = f"Here is a Google summary for {query}:\n{search_url}"
    bot.reply_to(message, response)

    # The movie database search
    result = movie_search(query)

    bot.send_message(chat_id, "Here is a breakdown from The Movie Database:\n"+result)


# to search the movie database
def movie_search(movie):
    url = f"https://api.themoviedb.org/3/search/movie?query=" + urllib.parse.quote(movie)
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }
    tmdb_search = requests.get(url, headers=headers)
    data = json.loads(tmdb_search.text)
    title = data["results"][0]["title"]
    popularity = data["results"][0]["popularity"]
    vote_count = data["results"][0]["vote_count"]
    vote_average = data["results"][0]["vote_average"]

    result = f"Title: {title}\nPopularity: {popularity}\nVote Count: {vote_count}\nVote Average: {vote_average}"
    return result


bot.infinity_polling()
