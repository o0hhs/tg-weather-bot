from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F, Bot, Dispatcher

from api.get_weather import get_weather_forecast
from api.get_cats import get

from datetime import datetime, date
import pytz

import keyboards as k
import db.requests as r

from db.requests import create_new_user
from db.models import async_main

from dotenv import load_dotenv

import asyncio

import logging

import os

class UserState(StatesGroup):
    choosing_city = State()
    custom_longitude = State()
    custom_latitude = State()
    from_main = State()
    
load_dotenv()
    
TOKEN=os.getenv('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    logging.warning(f"Бот был запущен пользователем. {message.from_user.username}, {message.from_user.id}")
    if await create_new_user(message.from_user.id, message.chat.id):
        await r.set_status(message.from_user.id, True)
        await message.answer_photo(photo=get(), caption=f'Привет, {message.from_user.full_name}, с этого момента каждый день я буду тебе отправлять погоду, с милой картинкой котика! Только для начала давай определимся, где ты живёшь.', reply_markup=k.start_kb())
        await send_daily_message(message.chat.id, message.from_user.id)
    else:
        await r.set_status(message.from_user.id, True)
        await message.answer_photo(photo=get(), caption=f'Привет, {message.from_user.full_name}, Рады тебя видеть!.', reply_markup=k.main_kb())
        await send_daily_message(message.chat.id, message.from_user.id)

@dp.message(Command('stop'))
async def stop_command(message: Message):
    logging.warning(f"Остановка {message.from_user.username}, {message.from_user.id}")
    await r.set_status(message.from_user.id, False)
    await message.answer_photo(photo=get(), caption=f'Прощай, {message.from_user.full_name}, будем ждать тебя снова! (Чтобы начать снова, напишите /start)')
    
@dp.message(F.text == "Оставновить бота⛔️")
async def stop_text(message: Message):
    logging.warning(f"Остановка {message.from_user.username}, {message.from_user.id}")
    await r.set_status(message.from_user.id, False)
    await message.answer_photo(photo=get(), caption=f'Прощай, {message.from_user.full_name}, будем ждать тебя снова! (Чтобы начать снова, напишите /start)')

@dp.message(Command('getnow'))
async def getnow_command(message: Message):
    logging.warning(f"Получение погоды (запрос от пользователя) {message.from_user.username}, {message.from_user.id}")
    try:    
        weather = await get_weather_forecast(message.from_user.id)
        await create_new_user(message.from_user.id, message.chat.id)
        await message.answer_photo(photo=get(), caption=f"Сегодня {date.today()}. Прогноз погоды на сегодня: День {weather['max_temp']}℃, Ночь {weather['min_temp']}℃, будет {weather['name']}")
    except Exception as e:
        await message.answer(text=f"Опачки, произошла ошибка: {e}.", reply_markup=k.start_kb())

@dp.message(F.text == "Получить погоду сейчас🌏")
async def getnow_text(message: Message):
    logging.warning(f"Получение погоды (запрос от пользователя) {message.from_user.username}, {message.from_user.id}")
    try:    
        weather = await get_weather_forecast(message.from_user.id)
        await create_new_user(message.from_user.id, message.chat.id)
        await message.answer_photo(photo=get(), caption=f"Сегодня {date.today()}. Прогноз погоды на сегодня: День {weather['max_temp']}℃, Ночь {weather['min_temp']}℃, будет {weather['name']}")
    except Exception as e:
        await message.answer(text=f"Опачки, произошла ошибка: {e}.", reply_markup=k.start_kb())

@dp.message(F.text == 'Найти свой город')
async def find_city(message: Message, state: FSMContext):
    logging.warning(f"Поиск города {message.from_user.username}, {message.from_user.id}")
    await state.set_state(UserState.choosing_city)
    await message.answer(text='Ну что, тогда давай поищем!',reply_markup=await k.cities())
    
@dp.message(F.text == 'Написать координаты')
async def set_custom_coordinates(message: Message, state: FSMContext):
    logging.warning(f"Ввод долготы {message.from_user.username}, {message.from_user.id}")
    await state.set_state(UserState.custom_longitude)
    await message.answer(text="Введите долготу (пример: 82.7893):")



@dp.message(UserState.custom_longitude)
async def custom_longitude(message: Message, state: FSMContext):
    logging.warning(f"Ввод широты {message.from_user.username}, {message.from_user.id}")
    try:
        await r.set_coordinates_to_user(message.from_user.id, None, message.text, None)
        await state.clear()
        await state.set_state(UserState.custom_latitude)
        await message.answer(text='Отлично! Теперь введите широту:')        
    except Exception as e:
        logging.error(f"Произошла ошибка, возможно пользователь ввел что-то другое, а не координаты. Ошибка: {e}")
        await state.clear()
        await message.answer(text='Видимо что-то пошло не так... может вы ввели что-то не то? давайте вернем вас назад ради приличия...', reply_markup=k.start_kb())

    
@dp.message(UserState.custom_latitude)
async def custom_latitude(message: Message, state: FSMContext):
    logging.warning(f"Установка координат {message.from_user.username}, {message.from_user.id}")
    try:
        await r.set_coordinates_to_user(message.from_user.id, None, None, message.text)
        await message.answer_photo(photo=get(), caption="Отлично, тогда, мы начинаем!!! Завтра (ну или сегодня просто чуть попозже >3) ты получишь погодную сводку в 8:00 по мск с милой картинкой котика!!!>>3", reply_markup=k.main_kb())
        await state.clear()
        await send_daily_message(message.chat.id, message.from_user.id)        
    except Exception as e:
        logging.error(f"Произошла ошибка, возможно пользователь ввел что-то другое, а не координаты. Ошибка: {e}")
        await state.clear()
        await message.answer(text='Видимо что-то пошло не так... может вы ввели что-то не то? давайте вернем вас назад ради приличия...', reply_markup=k.start_kb())
    
@dp.message(F.location)
async def location_handler(message: Message):
    logging.warning(f"Локация была получена {message.from_user.username}, {message.from_user.id}, {message.location.latitude}, {message.location.longitude}")
    latitude = message.location.latitude
    longitude = message.location.longitude
    await r.set_coordinates_to_user(message.from_user.id, None, longitude, latitude)
    await send_daily_message(message.chat.id, message.from_user.id)
    await message.answer_photo(photo=get(), caption="Отлично, тогда, мы начинаем!!! Завтра (ну или сегодня просто чуть попозже >3) ты получишь погодную сводку в 8:00 по мск с милой картинкой котика!!!>>3", reply_markup=k.main_kb())    
      
@dp.message(F.text == 'Изменить местоположение📍')
async def change_geo(message: Message):
    logging.warning(f"Смена гео {message.from_user.username}, {message.from_user.id}")
    await message.answer(text="Давай поменяем! Выбери каким образом ты укажешь местоположение:", reply_markup=k.start_kb(True))  

@dp.message(F.text == 'На главную')
async def turn_back(message: Message):
    logging.warning(f"На главную {message.from_user.username}, {message.from_user.id}")
    await message.answer(text="Возращаем на главную...", reply_markup=k.main_kb())    
    
@dp.message(UserState.choosing_city)
async def city_chosen(message: Message, state: FSMContext):
    logging.warning(f"Город был выбран: {message.text}. {message.from_user.username}, {message.from_user.id}")
    cities = await r.all_cities()
    cities_list = [city.title_ru for city in cities]
    chosen = message.text
    if chosen not in cities_list:
        await message.answer(text="Такого города нет в нашем списке.", reply_markup=k.start_kb())
        await state.clear()
        return
    try:
        await r.set_coordinates_to_user(message.from_user.id, chosen)
        await message.answer_photo(photo=get(),caption="Отлично, тогда, мы начинаем!!! Завтра (ну или сегодня просто чуть попозже >3) ты получишь погодную сводку в 8:00 по мск с милой картинкой котика!!!>>3", reply_markup=k.main_kb())
        await send_daily_message(message.chat.id, message.from_user.id)
        await state.update_data(city=chosen)
        await state.clear()
    except Exception as e:
        logging.error(f"Произошла ошибка, возможно пользователь ввел что-то другое, а не город. Ошибка: {e}")
        await state.clear()
        await message.answer(text='Видимо что-то пошло не так... может вы ввели что-то не то? давайте вернем вас на главную ради приличия...', reply_markup=k.main_kb())


async def send_message(chat_id, user):
    """Вспомогательная функция для отправки сообщения"""
    try:
        weather = await get_weather_forecast(user)
        await bot.send_photo(
            photo=get(),
            caption=f"Доброе утро! Сегодня {date.today()}. Прогноз погоды на сегодня: День {weather['max_temp']}℃, Ночь {weather['min_temp']}℃, будет {weather['name']}",
            chat_id=chat_id
        )
        logging.warning(f"Ежедневное сообщение отправлено для пользователя {user}")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")
    
async def send_daily_message(chat_id, user):
    logging.warning(f"Отправка рассылки была запущена, статус пользователя: {await r.get_user_status(user)}.")
    
    # Словарь для отслеживания отправленных сообщений
    sent_messages = {11: False, 2: False}  # для 11:27 и 11:02
    
    while await r.get_user_status(user):
        try:
            # Получаем текущее время в нужном часовом поясе
            now = datetime.now(pytz.timezone('Asia/Yekaterinburg'))
            current_time = now.time()
            current_hour = current_time.hour
            current_minute = current_time.minute
            
            # print(f"Текущее время: {current_time}")
            
            # Проверяем время 10:00
            if current_hour == 10 and current_minute == 0 and not sent_messages[11]:
                await send_message(chat_id, user)
                sent_messages[11] = True
                # Сбрасываем флаг для другого времени
                sent_messages[2] = False
            
            # Сбрасываем флаги в начале нового дня
            if current_hour == 0 and current_minute == 0:
                sent_messages = {11: False, 2: False}
            
            # Ждем 40 секунд перед следующей проверкой
            logging.info(f"ждем {sent_messages}")
            await asyncio.sleep(40)
            
        except Exception as e:
            logging.error(f"Ошибка в send_daily_message: {e}")
            await asyncio.sleep(60)




async def main():
    await async_main()
    print("Hello from python-cats-bot!")    
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
