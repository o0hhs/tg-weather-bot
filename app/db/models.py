from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, Boolean, Double, String, Time
from datetime import time

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
Session = async_sessionmaker(engine)

class Main(AsyncAttrs, DeclarativeBase):
    pass

class User(Main):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    longitude: Mapped[float] = mapped_column(Double, nullable=True)
    latitude: Mapped[float] = mapped_column(Double, nullable=True)
    time: Mapped[Time] = mapped_column(Time, default=time(10, 0))
    horoscop: Mapped[bool] = mapped_column(Boolean, default=False)
    brief_weather_report: Mapped[bool] = mapped_column(Boolean, default=False)
    
class City(Main):
    __tablename__ = 'cities'
    
    id: Mapped[int] = mapped_column(primary_key=True)    
    title_en: Mapped[str] = mapped_column(String)
    title_ru: Mapped[str] = mapped_column(String)  
    longitude: Mapped[float] = mapped_column(Double, nullable=True)
    latitude: Mapped[float] = mapped_column(Double, nullable=True)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Main.metadata.create_all)