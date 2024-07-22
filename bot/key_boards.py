from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


pre_start_button = KeyboardButton(text='/start')
send_batton = KeyboardButton(text='/send')

pre_start_clava = ReplyKeyboardMarkup(
    keyboard=[[pre_start_button]],
    resize_keyboard=True)



send_clava = ReplyKeyboardMarkup(
    keyboard=[[send_batton]],
    resize_keyboard=True)









