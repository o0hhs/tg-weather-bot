from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from db.requests import all_cities

def start_kb(from_main=False):
    kb_list = [
        [KeyboardButton(text="Найти свой город"), KeyboardButton(text="Отправить геопозицию", request_location=True)],
        [KeyboardButton(text="Написать координаты")]
    ]
    if from_main:
        kb_list.append([KeyboardButton(text="На главную")])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def main_kb():
    kb_list = [
        [KeyboardButton(text="Изменить местоположение📍"), KeyboardButton(text="Получить погоду сейчас🌏")],
         [KeyboardButton(text="Оставновить бота⛔️"),]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return keyboard

async def cities():
    cities = await all_cities()
    keyboard = ReplyKeyboardBuilder()
    for city in cities:
        keyboard.add(KeyboardButton(text=city.title_ru))
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder="Выберите город или напишите свой...")