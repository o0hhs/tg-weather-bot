from db.models import User, Session, City
from sqlalchemy import select
import asyncio

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
         
            
    
if __name__ == '__main__':
    asyncio.run(all_cities())
        