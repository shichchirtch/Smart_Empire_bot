from aiogram import Router, F, html
import asyncio
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command, StateFilter
from filters import PRE_START
from key_boards import pre_start_clava, send_clava
from lexicon import start_message
from aiogram.fsm.context import FSMContext
from FSM_states import FSM_ST
from postgres_functions import *

ch_router = Router()

@ch_router.message(~F.text)
async def delete_not_text_type_messages(message: Message):
    await message.delete()


@ch_router.message(CommandStart(), ~StateFilter(FSM_ST.wait))
async def process_start_command(message: Message,  state: FSMContext):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    data = await check_user_in_table(user_id)
    if not data:
        await insert_new_user_in_table(user_id, user_name)
        await state.set_state(FSM_ST.after_start)
        await message.answer(text=f'{html.bold(html.quote(user_name))}, '
                                  f'{start_message}',
                             parse_mode=ParseMode.HTML,
                             reply_markup=send_clava)
    else:
        await message.delete()

@ch_router.message(PRE_START())
async def before_start(message: Message):
    prestart_ant = await message.answer(text='Нажми на кнопку <b>start</b> !',
                                        reply_markup=pre_start_clava)
    await message.delete()
    await asyncio.sleep(4)
    await prestart_ant.delete()


@ch_router.message(Command(commands='send'), ~StateFilter(FSM_ST.wait))
async def set_send(message: Message, state: FSMContext):
    await message.answer('Посылайте текст следующим сообщением !',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSM_ST.accept)


@ch_router.message(~StateFilter(FSM_ST.wait), StateFilter(FSM_ST.accept))
async def send_me(message: Message, state: FSMContext):
    sending_data = message.text
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    join_text = f'User_id {user_id}, user_name  {user_name} send MESSAGE {sending_data}'
    await message.bot.send_message(chat_id=-1002226816025, text=join_text)
    await incremet_send_msg(user_id)
    await state.set_state(FSM_ST.wait)
    await message.answer("Ваше сообщение успешно отпралено ! Спасибо !")
    await asyncio.sleep(20)
    await state.set_state(FSM_ST.after_start)


@ch_router.message(StateFilter(FSM_ST.wait))
async def wait_handler(message: Message):
    att = await message.reply("Ваше сообщение успешно отправлено.\n"
                        "Если хотите отправить ещё одно - подождите полчаса")
    await asyncio.sleep(5)
    await message.delete()
    await att.delete()

@ch_router.message(StateFilter(FSM_ST.after_start))
async def buffer(message: Message):
    att = await message.answer('Хотите полсать сообщение ? Нажмите /send',
                         reply_markup=send_clava)
    await asyncio.sleep(5)
    await message.delete()
    await att.delete()



