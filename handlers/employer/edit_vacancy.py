import asyncio
import os

from aiogram.types import CallbackQuery, ContentType, FSInputFile
from aiogram import Router, F, Bot
from aiogram.filters import StateFilter, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from classes.Statesform import VacancyFormSteps as vfs
from keyboards.inline_keyboards import *

from classes import db_commands
from assets import texts
from utils.setcomands import set_cancel_edit_command, set_cancel_create_vacancy_command

router = Router()


async def send_preview(message: Message, state: FSMContext):
    data = await state.get_data()

    if (path := data.get("image")) == "0":
        path = "default_image.jpg"
    photo = FSInputFile(path=path)
    await message.answer_photo(photo=photo,
                               caption=await db_commands.dict_to_text(vacancy_values=data,
                                                                      type_descr="short"),
                               reply_markup=inkb_preview_more)

    await asyncio.sleep(0.2)
    await message.answer("Выберите, что вы хотите отредактировать", reply_markup=inkb_edit_vac)
    await state.set_state(vfs.confirm_create)


@router.callback_query(StateFilter(vfs.confirm_create), F.data == 'edit_employer')
async def callback_edit_employer(callback: CallbackQuery,
                                 state: FSMContext,
                                 bot: Bot):
    await callback.message.edit_text(text=texts.fill_employer)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_employer)


@router.callback_query(StateFilter(vfs.confirm_create), F.data == 'edit_job')
async def callback_edit_job(callback: CallbackQuery,
                            state: FSMContext,
                            bot: Bot):
    await callback.message.edit_text(text=texts.fill_job)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_job)


@router.callback_query(StateFilter(vfs.confirm_create), F.data == 'edit_salary')
async def callback_edit_salary(callback: CallbackQuery,
                               state: FSMContext,
                               bot: Bot):
    await callback.message.edit_text(text=texts.fill_salary)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_salary)


@router.callback_query(StateFilter(vfs.confirm_create), F.data == 'edit_minage')
async def callback_edit_min_age(callback: CallbackQuery,
                                state: FSMContext,
                                bot: Bot):
    await callback.message.edit_text(text=texts.fill_min_age)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_min_age)


@router.callback_query(StateFilter(vfs.confirm_create), F.data == 'edit_minexp')
async def callback_edit_min_exp(callback: CallbackQuery,
                                state: FSMContext,
                                bot: Bot):
    await callback.message.edit_text(text=texts.fill_min_exp)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_min_exp)


@router.callback_query(StateFilter(vfs.confirm_create), F.data == 'edit_date')
async def callback_edit_date(callback: CallbackQuery,
                             state: FSMContext,
                             bot: Bot):
    await callback.message.edit_text(text=texts.fill_date)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_date)


@router.callback_query(StateFilter(vfs.confirm_create), F.data == 'edit_short_dsp')
async def callback_edit_short_dsp(callback: CallbackQuery,
                                  state: FSMContext,
                                  bot: Bot):
    await callback.message.edit_text(text=texts.fill_short_dsp)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_short_dsp)


@router.callback_query(StateFilter(vfs.confirm_create), F.data == 'edit_long_dsp')
async def callback_edit_long_dsp(callback: CallbackQuery,
                                 state: FSMContext,
                                 bot: Bot):
    await callback.message.edit_text(text=texts.fill_long_dsp)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_long_dsp)


@router.callback_query(StateFilter(vfs.confirm_create), F.data == 'edit_image')
async def callback_edit_image(callback: CallbackQuery,
                              state: FSMContext,
                              bot: Bot):
    await callback.message.edit_text(text=texts.fill_new_image)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_image)
    photo = FSInputFile(path="default_image.jpg")
    await callback.message.answer_photo(photo=photo, caption=texts.edit_standard_image,
                                        reply_markup=inkb_set_standard_image)


@router.message(StateFilter(vfs.edit_employer, vfs.edit_job, vfs.edit_salary, vfs.edit_min_age,
                            vfs.edit_min_exp, vfs.edit_date, vfs.edit_short_dsp, vfs.edit_long_dsp, vfs.edit_image),
                Command(commands=['cancel']))
async def command_cancel_edit(message: Message,
                              state: FSMContext,
                              bot: Bot):
    await message.delete()
    await bot.edit_message_text(text=texts.mess12dsh,
                                reply_markup=inkb_edit_cancel_save,
                                chat_id=message.from_user.id,
                                message_id=message.message_id - 1)
    await state.set_state(vfs.confirm_create)


@router.message(StateFilter(vfs.edit_employer), F.text)
async def sent_employer(message: Message,
                        state: FSMContext,
                        bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)
    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"🔰 Указанная организация или физическое лицо"
                                     f"\n—————\n"
                                     f"<b><i>{message.text}</i></b>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)

    await message.delete()

    await message.answer(text=texts.edit_employer)
    await state.update_data(employer=message.text)
    await set_cancel_create_vacancy_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.message(StateFilter(vfs.edit_job), F.text)
async def sent_work_type(message: Message,
                         state: FSMContext,
                         bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"🔰 Указанная должность или работа"
                                     f"\n—————\n"
                                     f"<b><i>{message.text}</i></b>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)

    await message.delete()

    await message.answer(text=texts.edit_job)
    await state.update_data(work_type=message.text)
    await set_cancel_create_vacancy_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.message(StateFilter(vfs.edit_salary), F.text)
async def sent_salary(message: Message,
                      state: FSMContext,
                      bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"🔰 Указанная зарплата"
                                     f"\n—————\n"
                                     f"<b><i>{message.text}</i></b>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)

    await message.delete()

    await message.answer(text=texts.edit_salary)
    await state.update_data(salary=message.text)
    await set_cancel_create_vacancy_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.message(StateFilter(vfs.edit_min_age), F.text)
async def sent_min_age(message: Message,
                       state: FSMContext,
                       bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"🔰 Указанный минимальный возраст"
                                     f"\n—————\n"
                                     f"<b><i>{message.text}</i></b>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)
    await message.delete()

    await message.answer(text=texts.edit_minage)
    await state.update_data(min_age=message.text)
    await set_cancel_create_vacancy_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.message(StateFilter(vfs.edit_min_exp), F.text)
async def sent_min_exp(message: Message,
                       state: FSMContext,
                       bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)
    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"🔰 Указанный минимальный опыт работы"
                                     f"\n—————\n"
                                     f"<b><i>{message.text}</i></b>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)

    await message.delete()

    await message.answer(text=texts.edit_minexp)
    await state.update_data(min_exp=message.text)
    await set_cancel_create_vacancy_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.message(StateFilter(vfs.edit_date), F.text)
async def sent_datetime(message: Message,
                        state: FSMContext,
                        bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"🔰 Указанный период работы"
                                     f"\n—————\n"
                                     f"<b><i>{message.text}</i></b>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)
    await message.delete()

    await message.answer(text=texts.edit_date)
    await state.update_data(datetime=message.text)
    await set_cancel_create_vacancy_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.message(StateFilter(vfs.edit_short_dsp), F.text)
async def sent_short_dscr(message: Message,
                          state: FSMContext,
                          bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"🔰 Указанное краткое описание"
                                     f"\n—————\n"
                                     f"<b><i>{message.text}</i></b>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)

    await message.delete()

    await message.answer(text=texts.edit_short_dsp)
    await state.update_data(s_dscr=message.text)
    await set_cancel_create_vacancy_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.message(StateFilter(vfs.edit_long_dsp), F.text)
async def sent_long_dscr(message: Message,
                         state: FSMContext,
                         bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)
    message_to_edit_id = message.message_id - 1

    words: list = message.text.split(" ")
    answer: str = " ".join([word for word in words[:10]])

    await bot.edit_message_text(text=f"🔰 Указанное развёрнутое описание"
                                     f"\n—————\n"
                                     f"<i><b>{answer}" + f"{'...' if len(words) > 10 else ''}</b></i>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)

    await message.delete()

    await message.answer(text=texts.edit_long_dsp)
    await state.update_data(l_dscr=message.text)
    await set_cancel_create_vacancy_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.message(StateFilter(vfs.edit_image), F.photo | F.document)
async def sent_image(message: Message,
                     state: FSMContext,
                     bot: Bot):
    file_id = ""
    if message.content_type == ContentType.PHOTO:
        file_id = message.photo[-1].file_id
    elif message.content_type == ContentType.DOCUMENT:
        file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    extension = file_info.file_path.split(".")[-1].lower()
    if extension not in ["jpg", "jpeg", "png", "tiff", "tif"]:
        return await message.answer("Данный формат не поддерживается")

    data = await state.get_data()
    if (path := data.get("image")) != "0":
        os.remove(path)

    path = f"{file_info.file_id}.{extension}"
    await bot.download_file(file_info.file_path, path)
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 4)

    await message.delete()
    await message.answer("Выбрано пользовательское превью")

    await message.answer(text=texts.edit_image)
    await state.update_data(image=path)

    await set_cancel_create_vacancy_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.callback_query(StateFilter(vfs.edit_image), F.data == "set_standard_image")
async def set_standard_image(callback: CallbackQuery,
                             state: FSMContext,
                             bot: Bot):
    await state.set_state(vfs.confirm_create)
    await bot.delete_message(chat_id=callback.from_user.id,
                             message_id=callback.message.message_id - 1)
    await bot.delete_message(chat_id=callback.from_user.id,
                             message_id=callback.message.message_id - 2)
    await bot.delete_message(chat_id=callback.from_user.id,
                             message_id=callback.message.message_id - 3)
    data = await state.get_data()

    if (path := data.get("image")) != "0":
        os.remove(path)

    await callback.message.delete()
    await callback.message.answer("🔰 Выбрана картинка по умолчанию")

    await callback.message.answer(text=texts.edit_image)
    await state.update_data(image="0")
    await set_cancel_create_vacancy_command(bot, callback.message.from_user.id)

    await send_preview(message=callback.message, state=state)
