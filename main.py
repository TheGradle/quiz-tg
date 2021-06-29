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
    Definition("балда", "великий з довгим держаком молот"), 
    Definition("родзинка", "сушена виноградина"), 
    Definition("чхання", "Людські здібності досить великі. Наприклад, ми можемо власними силами розігнати повітряний потік до 150-170 км / год. В процесі чого людина здатна зробити такий повітряний потік?"),
    Definition("правда", "Польський вчений-математик Гуго Діонісій Штейнгауз, що прославився також своїми афоризмами, говорив: «Комплімент жінці повинен бути правдивіше, ніж ...»"),
    Definition("сковорода", "Що використовували в Китаї для прасування білизни замість праски?"),
    Definition("балакучість", "За традицією в Китаї чоловік може в односторонньому порядку оголосити про розірвання шлюбу за сімейними обставинами. Назвіть одну з причин для цього."),
    Definition("підліток", "В Австралії на парковках біля деяких торгових центрів по ночах і вечорами включають класичну музику, щоб відлякати когось. Кого?"),
    Definition("війна", "Якого слова немає в мові народів Арктики?")
]

def GetRandomWord():
    return words[randint(0, 7)]

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

    if message.text[0] == "!":
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
    elif message.text == "/stop@quizo_ua_bot" or message.text[1:] == "/stop":
        stop_help(message)
    else:
        bot.register_next_step_handler(message, members_step)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling()