from db.models import User, Session, City
from sqlalchemy import select
import asyncio
import json
import os
from typing import List, Dict
from pathlib import Path

async def create_new_user(tg_id:int, chat_id:int) -> bool:
    async with Session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == tg_id))
        if not user:
            session.add(User(telegram_id=tg_id, is_active=True, chat_id=chat_id))
            await session.commit()
            return True
        return False
            
async def create_new_city(title_en, title_ru, longitude, latitude) -> None:
    async with Session() as session:
        session.add(City(title_en=title_en, title_ru=title_ru, longitude=longitude, latitude=latitude))
        await session.commit()

async def all_cities():
    async with Session() as session:
        return await session.scalars(select(City))
    
async def set_coordinates_to_user(user, title_ru=None, longitude=None, latitude=None):
    async with Session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == user))
        if not user:
            session.add(User(telegram_id=user, is_active=True))
            await session.commit()
        if title_ru is not None:
            city = await session.scalar(select(City).where(City.title_ru == title_ru))
            if not city:
                raise Exception
            user.longitude = city.longitude
            user.latitude = city.latitude
        if longitude is not None:
            user.longitude = longitude
        elif latitude is not None:
            user.latitude = latitude
        await session.commit()
        
async def get_user_coordinates(user):
    async with Session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == user))
        user_coordinates = {'longitude':user.longitude,
                            'latitude':user.latitude}
        return user_coordinates

async def get_user_status(user):
    async with Session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == user))
        user_is_active = user.is_active
        if user_is_active == 1:
            return True
        else:
            return False

async def get_status_of_all_users():
    async with Session() as session:
        users = await session.scalars(select(User))
        return users
        
async def set_status(user, status: bool) -> None:
    async with Session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == user))
        user.is_active = status
        await session.commit()
         
async def load_cities_from_json(json_path: str = "cities.json"):
    script_dir = Path(__file__).parent.parent.parent
    json_path = script_dir / json_path
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Файл {json_path} не найден")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            cities_data: List[Dict] = json.load(f)
        
        if not isinstance(cities_data, list):
            raise ValueError("JSON должен содержать список городов")
        
        async with Session() as session:
            result = await session.execute(select(City.title_en))
            existing_cities = {city[0] for city in result.scalars().all()}
            cities_to_add = []
            for city_data in cities_data:
                required_fields = ['title_en', 'title_ru']
                for field in required_fields:
                    if field not in city_data:
                        raise ValueError(f"В данных города отсутствует обязательное поле: {field}")

                if city_data['title_en'] in existing_cities:
                    print(f"Город {city_data['title_en']} уже существует в БД, пропускаем")
                    continue
                
                # Создаем объект города
                city = City(
                    title_en=city_data['title_en'],
                    title_ru=city_data['title_ru'],
                    longitude=city_data.get('longitude'),  
                    latitude=city_data.get('latitude')
                )
                cities_to_add.append(city)
            
            # Добавляем города в сессию
            if cities_to_add:
                session.add_all(cities_to_add)
                await session.commit()
                print(f"Успешно добавлено {len(cities_to_add)} городов")
            else:
                print("Нет новых городов для добавления")
                
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка при чтении JSON файла: {e}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке городов: {e}")
            
    
if __name__ == '__main__':
    asyncio.run(load_cities_from_json())
        