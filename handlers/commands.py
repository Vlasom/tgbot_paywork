from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from fsm.statesform import StapesForm as sf

from keyboards.inline_keyboards import *
from classes import User, Vacancy, vac_commands, db_commands
import asyncio
from assets import texts
__all__ = ["command_start", "command_choice", "command_create_vacancy"]

router = Router()


@router.message(Command(commands=['start']))
async def command_start(message: Message, state: FSMContext, user: User):
    if await state.get_state() is None:
        await message.reply(texts.welcome_text)
        await asyncio.sleep(0.3)
        await message.answer(text=texts.employ_or_employer, reply_markup=inkb_employ_employer)

        await db_commands.add_user_to_db(user)
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
async def command_show_favorites(message: Message, state: FSMContext, user: User):
    if await state.get_state() is None:

        user_liked_vacancies = await vac_commands.get_user_likes(user)

        if user_liked_vacancies:
            for vacancy_values in user_liked_vacancies:
                vacancy = Vacancy(values=await db_commands.row_to_dict(vacancy_values))

                text = await vac_commands.to_text(vacancy=vacancy,
                                                  type_descr="short")

                await message.answer(text=text,
                                     reply_markup=await create_inkb(id=vacancy.id,
                                                                    is_next=False,
                                                                    btn_like_nlike="nlike",
                                                                    btn_more_less="more"))
        else:
            await message.answer(texts.no_favorites)

    else:
        await message.answer(texts.default_state_warn)


@router.message(Command(commands=['my_vacancies']))
async def command_show_created_vacancies(message: Message, state: FSMContext, user: User):

    if await state.get_state() is None:

        created_user_vacancies = await vac_commands.get_user_creates(user)

        if created_user_vacancies:
            for vacancy_values in created_user_vacancies:
                vacancy = Vacancy(values=await db_commands.row_to_dict(vacancy_values))

                text = await vac_commands.to_text(vacancy=vacancy,
                                                  type_descr="short")

                await message.answer(text=text,
                                     reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                 btn_more_less="more"))
        else:
            await message.answer(texts.no_created)

    else:
        await message.answer(texts.default_state_warn)