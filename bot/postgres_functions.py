from database import session_marker, User
from sqlalchemy import select

async def insert_new_user_in_table(user_tg_id: int, name: str):
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        needed_data = query.scalar()
        if not needed_data:
            print('Now we are into first function')
            new_us = User(tg_us_id=user_tg_id, user_name=name)
            session.add(new_us)
            await session.commit()

async def check_user_in_table(user_tg_id:int):
    """Функция проверяет есть ли юзер в БД"""
    async with session_marker() as session:
        print("Work check_user Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        data = query.one_or_none()
        return data

async def incremet_send_msg(user_id:int):
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.tg_us_id == user_id))
        needed_data = query.scalar()
        needed_data.sending_msg += 1
        await session.commit()

