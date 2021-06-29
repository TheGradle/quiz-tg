# -*- coding: utf-8 -*-
import telebot
from telebot import types

bot=telebot.TeleBot("1619514050:AAEmmhl52Z4NEnJlY4keTytSOisB9F2uNJg")
#channel="-1001347996353"

@bot.message_handler(commands=['start'])
def send_message(message):
    bot.send_message(message.chat.id, "👋 Вітаю, " + message.from_user.first_name + ".\nЦе бот вікторина, я задаю вам питання, а ви разом з друзями відгадуєте!")

@bot.message_handler(commands=['help'])
def send_message(message):
    bot.send_message(message.chat.id, "❗️*Бот працює в тестовому режимі.*\n\nДля початку гри додайте бота у вашу групу та зробіть його адміном, далі введіть команду /game.", parse_mode="Markdown", disable_web_page_preview=True)

@bot.message_handler(commands=['game'])
def handle_all_message(message):
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.send_message(message.chat.id, "❗️ Додайте бота до групи, для детальної інформації введіть /help.")
    else:
        bot.send_message(message.chat.id, "❗️*Бот працює в тестовому режимі.*", parse_mode="Markdown", disable_web_page_preview=True)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling()