from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from fsm.statesform import StapesForm as sf

from keyboards.inline_keyboards import *
from objects import *

__all__ = ["command_start", "command_choice", "command_create_vacancy"]

router = Router()


@router.message(Command(commands=['start']))
async def command_start(message: Message, bot: Bot, state: FSMContext):
    if await state.get_state() is None:
        await message.reply(texts.welcome_text)
        await asyncio.sleep(0.3)
        await message.answer(text=texts.employ_or_employer, reply_markup=inkb_employ_employer)

        user = User(tg_id=message.from_user.id,
                    username=message.from_user.username,
                    fullname=message.from_user.full_name)

        await user_commands.add_to_db(user)
    else:
        await message.answer(text=texts.default_state_warn)


@router.message(Command(commands=['choice']))
async def command_choice(message: Message, state: FSMContext):
    if await state.get_state() is None:
        await message.reply(text=texts.employ_or_employer, reply_markup=inkb_employ_employer)
    else:
        await message.answer(texts.default_state_warn)


@router.message(Command(commands=['create_vacancy']))
async def command_create_vacancy(message: Message, state: FSMContext):
    if await state.get_state() is None:
        await message.answer(texts.start_create)
        await message.answer(texts.fill_employer)
        await state.set_state(sf.fill_employer)
    else:
        await message.answer(texts.default_state_warn)


@router.message(Command(commands=['favorites']))
async def command_show_favorites(message: Message, state: FSMContext):
    if await state.get_state() is None:

        user = User(tg_id=message.from_user.id)

        user_liked_vacancies = await vac_commands.get_user_likes(user)

        if user_liked_vacancies:
            for vacancy in user_liked_vacancies:

                text = await vac_commands.to_text(vacancy=vacancy,
                                                  type_descr="short")
                liked_vacancy_id = vacancy[0]

                await message.answer(text=text,
                                     reply_markup=await create_inkb(id=liked_vacancy_id,
                                                                    is_next=False,
                                                                    btn_like_nlike="nlike",
                                                                    btn_more_less="more"))
        else:
            await message.answer(texts.no_favorites)

    else:
        await message.answer(texts.default_state_warn)


@router.message(Command(commands=['my_vacancies']))
async def command_show_created_vacancies(message: Message, state: FSMContext):

    if await state.get_state() is None:

        user = User(tg_id=message.from_user.id)
        created_user_vacancies = await vac_commands.get_user_creates(user)

        if created_user_vacancies:
            for vacancy in created_user_vacancies:
                text = await vac_commands.to_text(vacancy=vacancy, type_descr="short")

                created_vacancy_id = vacancy[0]
                await message.answer(text=text,
                                     reply_markup=await create_inkb(id=created_vacancy_id,
                                                                    is_next=False,
                                                                    btn_like_nlike="like",
                                                                    btn_more_less="more"))
        else:
            await message.answer(texts.no_created)

    else:
        await message.answer(texts.default_state_warn)