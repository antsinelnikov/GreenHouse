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

# setup

# создаём объект для работы с сенсором
sensor3_temp = W1ThermSensor()
sensor4_temp = W1ThermSensor()

# создаём объект для работы с расширителем портов
exp = gpioexp.gpioexp()

# пин к которому подключен датчик влажности почвы
# любой GPIO пин платы расширения Troyka Cap
pinSensor1 = 1
pinSensor2 = 2

# end setup


bot = telebot.TeleBot('6031969731:AAGpj4dF2qd1nNobJIWZdh2bQApWTdEMTVE')

air_temperature = ''
soil_moisture = ''
air_humidity = ''
air_temperature_now = ''
soil_moisture_now = ''
air_humidity_now = ''

def read_sensors():
    # считываем состояние датчика влажности почвы
    valueSensor1 = exp.analogRead(pinSensor1) * 100
    valueSensor2 = exp.analogRead(pinSensor2) * 100
    valueSensor_of_soil_moisture_now = (valueSensor1 + valueSensor2)/2

    # считываем данные температуры воздуха с датчика
    temperature = (sensor3_temp.get_temperature() + sensor4_temp.get_temperature())/2

    # выводим значения в консоль каждую секунду
    print('Value sensor: ', round(valueSensor_of_soil_moisture_now), ' %')
    print(temperature)
    return temperature, valueSensor_of_soil_moisture_now

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