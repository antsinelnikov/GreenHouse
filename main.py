#Веб-интерфейс для записи данных на устройство, реализованный за счёт Telegram Бота

import telebot
import asyncio
import time
from time import sleep
import RPi.GPIO as GPIO
# библиотека для работы с расширителем портов GPIO Expander на плате Troyka Cap
import gpioexp
import W1ThermSensor
from w1thermsensor import W1ThermSensor

from telebot import types



bot = telebot.TeleBot('')

air_temperature = ''
soil_moisture = ''
air_humidity = ''
air_temperature_now = ''
soil_moisture_now = ''
air_humidity_now = ''

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Ввести данные")
    btn2 = types.KeyboardButton("Текущие показания")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Привет! Я твоя умная теплица! Помоги мне настроить данные для твоего растения!'
                     , reply_markup=markup)

    if message.text == "Ввести данные":
        bot.send_message(message.from_user.id, "Введи температуру воздуха:")
        bot.register_next_step_handler(message, get_air_temperature)
    elif message.text == "Текущие показания":
        bot.send_message(message.from_user_id,
                         'Итак, температура воздуха: ' + air_temperature + ', влажность почвы: ' + soil_moisture + ', влажность воздуха: ' + air_humidity, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Ввести данные")
        btn2 = types.KeyboardButton("Текущие показания")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
                         'Вы вернулись в главное меню' + str(i),
                         reply_markup=markup)

    if message.text == "Ввести данные":
        bot.send_message(message.from_user.id, "Введите температуру воздуха:")
        bot.register_next_step_handler(message, get_air_temperature)
    elif message.text == "Текущие показания":
        bot.send_message(message.from_user_id,
                         'Итак, температура воздуха: ' + temperature + ', влажность почвы: ' + valueSensor_of_soil_moisture_now + ', влажность воздуха: ' + air_humidity)


def get_air_temperature(message):
    global air_temperature
    air_temperature = message.text
    bot.send_message(message.from_user.id, 'Введите влажность почвы:')
    bot.register_next_step_handler(message, get_soil_moisture)


def get_soil_moisture(message):
    global soil_moisture
    soil_moisture = message.text
    bot.send_message(message.from_user.id, 'Введите влажность воздуха:')
    bot.register_next_step_handler(message, get_air_humidity)


def get_air_humidity(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn1)
    global air_humidity
    air_humidity = message.text
    bot.send_message(message.from_user.id,
                     'Итак, температура воздуха: ' + air_temperature + ', влажность почвы: ' + soil_moisture + ', влажность воздуха: ' + air_humidity,
                     reply_markup=markup)

bot.polling(none_stop=True)
