from aiogram.types import Message, ErrorEvent, FSInputFile
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import default_state
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command, ExceptionTypeFilter

from keyboards.inline_keyboards import *
from classes import *
from classes.Statesform import Test
from assets import texts

import asyncio

router = Router()


@router.message(Command(commands=["test"]))
async def test(message: Message, state: FSMContext):
    await message.answer("отправь фото")
    await state.set_state(Test.test11)


@router.message(StateFilter(Test.test11))
async def test(message: Message, state: FSMContext, bot: Bot):
    file_id = message.document.file_id
    await message.answer(file_id)
    file_info = await bot.get_file(file_id)
    await message.answer(file_info.model_dump_json())
    path = file_info.file_id+ "." + file_info.file_path.split(".")[1]
    downloaded_file = await bot.download_file(file_info.file_path, path)
    await message.answer(f"{downloaded_file}")
    ppphoto = FSInputFile(path=path)
    await message.answer_photo(photo=ppphoto, caption="Это отправлено с помощью FSInputFile")
    await message.answer_photo(photo=file_id, caption="Это отправлено с помощью file_id")

    await state.clear()


@router.message(~StateFilter(default_state), ~F.text)
async def command_cancel_create(message: Message):
    await message.answer(texts.warning_msg)


@router.message(Command(commands=[""]))
async def command_cancel_create(message: Message):
    await message.answer(texts.command_doesnt_exist)


@router.message(StateFilter(default_state))
async def command_cancel_create(message: Message, user: User):
    markup = inkb_verified_users if await redis_commands.check_verification(user) else inkb_not_verified_users
    await message.answer(texts.random_msg, reply_markup=markup)


# @router.error(ExceptionTypeFilter(TelegramBadRequest), F.update.message.as_("message"))
# async def command_cancel_create(event: ErrorEvent, message: Message):
#     await message.answer(texts.waning_u_are_stupid)
