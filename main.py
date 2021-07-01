# -*- coding: utf-8 -*-
from requests.models import codes
import telebot
from telebot import types
from random import randint

bot = telebot.TeleBot("1619514050:AAEmmhl52Z4NEnJlY4keTytSOisB9F2uNJg")

class Definition:
    def __init__(self, word, definition):
        self.word = word
        self.definition = definition

words = [
    Definition("венера", "Яка планета є найгарячішою в Сонячній системі?"), 
    Definition("землетруси", "Яке стихійне лихо вимірюється за шкалою Ріхтера?"), 
    Definition("меланін", "Як називається речовина, яка надає шкірі та волоссю пігмент?"),
    Definition("меркурій", "Яка планета найближча до Сонця?"),
    Definition("галілей", "Хто перший побачив супутники Юпітера (прізвище)?"),
    Definition("гамофобія", "Страх бути зобов’язаним чи одружитися відомий як що?"),
    Definition("блондинки", "У кого більше волосяних фолікулів, блондинок чи брюнеток?"),
    Definition("січень", "У якому місяці Земля найближча до сонця?"),
    Definition("кератин", "З якої речовини зроблені нігті?"),
    Definition("дипси", "Хто з Телепузиків був зеленим?"),
    Definition("синій", "День Святого Патріка спочатку асоціювався з яким кольором?"),
    Definition("маркс", "Останніми словами соціалістичного письменника були: «Останні слова для дурнів, які недостатньо сказали» (прізвище)?"),
    Definition("белфаст", "У якому місті був побудований Титанік?"),
    Definition("християнство", "Яка релігія є найпоширенішою релігією у світі?"),
    Definition("франція", "Більшість пап були італійцями. Яка країна має 2-е місце за кількістю пап?"),
    Definition("арес", "Хто був грецьким богом війни?"),
    Definition("північ", "Що означає «N» в НАТО (українською)?"),
    Definition("ріанна", "У 2017 році, як звали жінку-виконавцю, яка мала найбільшу кількість потоків на Spotify?"),
    Definition("серце", "Який орган має чотири камери?"),
    Definition("шкіра", "Який орган є найбільшим в організмі людини?"),
    Definition("печінка", "Який найбільший внутрішній орган в організмі людини?"),
    Definition("вії", "Яке волосся на тілі людини сіріє в останню чергу?"),
    Definition("печінка", "Який орган виробляє білірубін?"),
    Definition("термометр", "Який медичний прилад був винайдений Санкторіусом у 1612 році?"),
    Definition("гемофілія", "Яка хвороба крові також відома як “королівська хвороба”?")
]

def GetRandomWord():
    return words[randint(0, 24)]

def GetHashWord(word):
    code = ""
    
    while (len(code) != len(word)):
        code += "#"

    return code

def hasLetter(letter, word):
    for i in word:
        if letter == i:
            return True

    return False

def hasHash(code):
    for i in code:
        if i == "#":
            return True

    return False

def EditHashWord(letter, code, word):
    newcode = list(code)
    
    i = 0
    while i < len(word):
        if letter == word[i]:
            newcode[i] = letter
        i += 1
    
    str = ''.join(newcode)
    return str

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
        quiz = GetRandomWord()
        global code
        code = GetHashWord(quiz.word)
        global answer
        answer = quiz.word
        bot.send_message(message.chat.id, "🤔 Почнемо! Якщо ви хочете зупинити гру завчасно напишіть /stop.\nВаше завдання відгадати наступне:\n*" + quiz.definition + "*\n" + code, parse_mode="Markdown")
        bot.register_next_step_handler(message, members_step)

@bot.message_handler(commands=['stop'])
def stop_help(message):
    global answer
    
    bot.send_message(message.chat.id, "Відповідь: " + answer)
    stop_game(message)

def stop_game(message):
    bot.send_message(message.chat.id, "❗️Гру завершено!")

def members_step(message):
    global code
    global answer

    if message.text and message.text[0] == "!":
        if message.text[1:] == answer:
            bot.reply_to(message, "🥳 Тааак! Молодці, цьом-цьом ^^")
            stop_game(message)
        elif hasLetter(message.text[1:], answer) == True:
            code = EditHashWord(message.text[1:], code, answer)
            if hasHash(code):
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