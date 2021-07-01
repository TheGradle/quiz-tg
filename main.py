# -*- coding: utf-8 -*-
from requests.models import codes
import telebot
from telebot import types
import funcs
import tgtoken

bot = telebot.TeleBot(tgtoken.TOKEN)

global game_check
game_check = False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "👋 Вітаю.\nЦе бот вікторина, я задаю вам питання, а ви разом з друзями відгадуєте!")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "❗️*Бот працює в тестовому режимі.*\n\nДля початку гри додайте бота у вашу групу та зробіть його адміном, далі введіть команду /game. Хто і в якій черзі буде називати літери - мені пофік, я не знаю як це контролювати.\n\n*Пишіть маленькі літери!*\n*Слово чи літеру пишіть починаючи зі знаку \"!\"*", parse_mode="Markdown")

@bot.message_handler(commands=['game'])
def start_game(message):
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.send_message(message.chat.id, "❗️Додайте бота до групи, для детальної інформації введіть /help.")
    else:
        quiz = funcs.GetRandomWord()
        global code
        code = funcs.GetHashWord(quiz.word)
        global answer
        answer = quiz.word
        global game_check
        game_check = True
        bot.send_message(message.chat.id, "🤔 Почнемо! Якщо ви хочете зупинити гру завчасно напишіть /stop. Нагадую: вводіть літеру або слово починаючи зі знаку \"!\". Будьте ввічливими та грайте по черзі.\n\nВаше завдання відгадати наступне:\n*" + quiz.definition + "*\n" + code, parse_mode="Markdown")
        bot.register_next_step_handler(message, members_step)

@bot.message_handler(commands=['stop'])
def stop_help(message):
    global game_check
    
    if game_check:
        global answer
    
        bot.send_message(message.chat.id, "Відповідь: " + answer)
        stop_game(message)
    else:
        bot.send_message(message.chat.id, "🤨 Хммм...\nА я думав, що не можна закінчити гру, яка не розпочиналась")

def stop_game(message):
    bot.send_message(message.chat.id, "❗️Гру завершено!")
    global game_check
    game_check = False

def members_step(message):
    global code
    global answer

    if message.text and message.text[0] == "!" and game_check:
        if message.text[1:] == answer:
            bot.reply_to(message, "🥳 Тааак! Молодці, цьом-цьом ^^")
            stop_game(message)
        elif funcs.hasLetter(message.text[1:], answer) == True:
            code = funcs.EditHashWord(message.text[1:], code, answer)
            if funcs.hasHash(code):
                bot.reply_to(message, "Є таке!\n" + code)
                bot.register_next_step_handler(message, members_step)
            else:
                bot.reply_to(message, "Отож: " + code)
                bot.send_message(message.chat.id, "🥳 Ну от, відстрілялися, красавииииииии")
                stop_game(message)
        else:
            bot.reply_to(message, "Ніт!")
            bot.register_next_step_handler(message, members_step)
    elif message.text == "/stop@quizo_ua_bot" or message.text == "/stop":
        stop_help(message)
    else:
        bot.register_next_step_handler(message, members_step)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling()