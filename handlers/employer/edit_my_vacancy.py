from aiogram.types import CallbackQuery, Message, ContentType, BufferedInputFile
from aiogram.filters import StateFilter, Command
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from keyboards.inline_keyboards import *
from filters.is_edit_my import IsEditMy

from assets import texts
from classes import *

from classes.Statesform import VacancyFormSteps as vfs

router = Router()
router.message.filter(IsEditMy())


async def send_edited_vacancy(message: Message, state: FSMContext):
    data = await state.get_data()
    vacancy = Vacancy(id=data["id"])
    row = await db_commands.get_row_by_id(vacancy.id)
    vacancy.values = await db_commands.row_to_dict(row)

    photo = BufferedInputFile(row[9], filename="")
    vacancy.text = await vac_commands.to_text(vacancy, type_descr="short")
    await message.answer_photo(photo=photo,
                               caption=vacancy.text,
                               reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                           btn_more_less="more"))


@router.callback_query(F.data.startswith("my_edit_employer"))
async def callback_edit_employer(callback: CallbackQuery,
                                 state: FSMContext):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[10][0].callback_data.split("_")[1]
    await callback.message.delete()
    await state.update_data(id=vacancy.id)
    await callback.message.answer(texts.my_editing_vacancy)
    await callback.message.send_copy(chat_id=callback.message.chat.id,
                                     reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                 btn_more_less=btn_more_less))
    await callback.message.answer(texts.fill_employer)
    await state.set_state(vfs.edit_employer)


@router.callback_query(F.data.startswith('my_edit_job'))
async def callback_edit_job(callback: CallbackQuery,
                            state: FSMContext):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[10][0].callback_data.split("_")[1]
    await callback.message.delete()
    await state.update_data(id=vacancy.id)
    await callback.message.answer(texts.my_editing_vacancy)
    await callback.message.send_copy(chat_id=callback.message.chat.id,
                                     reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                 btn_more_less=btn_more_less))
    await callback.message.answer(texts.fill_job)
    await state.set_state(vfs.edit_job)


@router.callback_query(F.data.startswith('my_edit_salary'))
async def callback_edit_salary(callback: CallbackQuery,
                               state: FSMContext):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[10][0].callback_data.split("_")[1]
    await callback.message.delete()
    await state.update_data(id=vacancy.id)
    await callback.message.answer(texts.my_editing_vacancy)
    await callback.message.send_copy(chat_id=callback.message.chat.id,
                                     reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                 btn_more_less=btn_more_less))
    await callback.message.answer(texts.fill_salary)
    await state.set_state(vfs.edit_salary)


@router.callback_query(F.data.startswith('my_edit_minage'))
async def callback_edit_min_age(callback: CallbackQuery,
                                state: FSMContext):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[10][0].callback_data.split("_")[1]
    await callback.message.delete()
    await state.update_data(id=vacancy.id)
    await callback.message.answer(texts.my_editing_vacancy)
    await callback.message.send_copy(chat_id=callback.message.chat.id,
                                     reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                 btn_more_less=btn_more_less))
    await callback.message.answer(texts.fill_min_age)
    await state.set_state(vfs.edit_min_age)


@router.callback_query(F.data.startswith('my_edit_minexp'))
async def callback_edit_min_exp(callback: CallbackQuery,
                                state: FSMContext):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[10][0].callback_data.split("_")[1]
    await callback.message.delete()
    await state.update_data(id=vacancy.id)
    await callback.message.answer(texts.my_editing_vacancy)
    await callback.message.send_copy(chat_id=callback.message.chat.id,
                                     reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                 btn_more_less=btn_more_less))
    await callback.message.answer(texts.fill_min_exp)
    await state.set_state(vfs.edit_min_exp)


@router.callback_query(F.data.startswith('my_edit_date'))
async def callback_edit_date(callback: CallbackQuery,
                             state: FSMContext):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[10][0].callback_data.split("_")[1]
    await callback.message.delete()
    await state.update_data(id=vacancy.id)
    await callback.message.answer(texts.my_editing_vacancy)
    await callback.message.send_copy(chat_id=callback.message.chat.id,
                                     reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                 btn_more_less=btn_more_less))
    await callback.message.answer(texts.fill_date)
    await state.set_state(vfs.edit_date)


@router.callback_query(F.data.startswith('my_edit_short_dsp'))
async def callback_edit_short_dsp(callback: CallbackQuery,
                                  state: FSMContext):
    vacancy = Vacancy(id=int(callback.data.split("_")[4]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[10][0].callback_data.split("_")[1]
    await callback.message.delete()
    await state.update_data(id=vacancy.id)
    await callback.message.answer(texts.my_editing_vacancy)
    await callback.message.send_copy(chat_id=callback.message.chat.id,
                                     reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                 btn_more_less=btn_more_less))
    await callback.message.answer(texts.fill_short_dsp)
    await state.set_state(vfs.edit_short_dsp)


@router.callback_query(F.data.startswith('my_edit_long_dsp'))
async def callback_edit_long_dsp(callback: CallbackQuery,
                                 state: FSMContext):
    vacancy = Vacancy(id=int(callback.data.split("_")[4]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[10][0].callback_data.split("_")[1]
    await callback.message.delete()
    await state.update_data(id=vacancy.id)
    await callback.message.answer(texts.my_editing_vacancy)
    await callback.message.send_copy(chat_id=callback.message.chat.id,
                                     reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                 btn_more_less=btn_more_less))
    await callback.message.answer(texts.fill_long_dsp)
    await state.set_state(vfs.edit_long_dsp)


@router.callback_query(F.data.startswith('my_edit_image'))
async def callback_edit_long_dsp(callback: CallbackQuery,
                                 state: FSMContext):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[10][0].callback_data.split("_")[1]
    await callback.message.delete()
    await state.update_data(id=vacancy.id)
    await callback.message.answer(texts.my_editing_vacancy)
    await callback.message.send_copy(chat_id=callback.message.chat.id,
                                     reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                 btn_more_less=btn_more_less))
    await callback.message.answer(texts.fill_new_image)
    await state.set_state(vfs.edit_image)


@router.message(StateFilter(vfs.edit_employer, vfs.edit_job, vfs.edit_salary, vfs.edit_min_age,
                            vfs.edit_min_exp, vfs.edit_date, vfs.edit_short_dsp, vfs.edit_long_dsp, vfs.edit_image),
                Command(commands=['cancel']))
async def undo_edit(message: Message,
                    state: FSMContext):
    await message.answer(texts.undo_editing)
    await state.clear()


@router.message(StateFilter(vfs.edit_employer), F.text)
async def send_job(message: Message,
                   state: FSMContext,
                   bot: Bot):
    data = await state.get_data()
    vacancy = Vacancy(id=data["id"])
    await vac_commands.edit_vacancy_data(vacancy, message.text, "employer")
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)
    await message.answer(text=texts.edit_employer)
    await send_edited_vacancy(message, state)
    await state.clear()


@router.message(StateFilter(vfs.edit_job), F.text)
async def send_job(message: Message,
                   state: FSMContext,
                   bot: Bot):
    data = await state.get_data()
    vacancy = Vacancy(id=data["id"])
    await vac_commands.edit_vacancy_data(vacancy, message.text, "work_type")
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)
    await message.answer(text=texts.edit_employer)
    await send_edited_vacancy(message, state)
    await state.clear()


@router.message(StateFilter(vfs.edit_salary), F.text)
async def send_min_age(message: Message,
                       state: FSMContext,
                       bot: Bot):
    data = await state.get_data()
    vacancy = Vacancy(id=data["id"])
    await vac_commands.edit_vacancy_data(vacancy, message.text, "salary")
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)
    await message.answer(text=texts.edit_employer)
    await send_edited_vacancy(message, state)
    await state.clear()


@router.message(StateFilter(vfs.edit_min_age), F.text)
async def send_min_exp(message: Message,
                       state: FSMContext,
                       bot: Bot):
    data = await state.get_data()
    vacancy = Vacancy(id=data["id"])
    await vac_commands.edit_vacancy_data(vacancy, message.text, "min_age")
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)
    await message.answer(text=texts.edit_employer)
    await send_edited_vacancy(message, state)
    await state.clear()


@router.message(StateFilter(vfs.edit_min_exp), F.text)
async def send_date(message: Message,
                    state: FSMContext,
                    bot: Bot):
    data = await state.get_data()
    vacancy = Vacancy(id=data["id"])
    await vac_commands.edit_vacancy_data(vacancy, message.text, "min_exp")
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)
    await message.answer(text=texts.edit_employer)
    await send_edited_vacancy(message, state)
    await state.clear()


@router.message(StateFilter(vfs.edit_date), F.text)
async def send_short_dsp(message: Message,
                         state: FSMContext,
                         bot: Bot):
    data = await state.get_data()
    vacancy = Vacancy(id=data["id"])
    await vac_commands.edit_vacancy_data(vacancy, message.text, "datetime")
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)
    await message.answer(text=texts.edit_employer)
    await send_edited_vacancy(message, state)
    await state.clear()


@router.message(StateFilter(vfs.edit_short_dsp), F.text)
async def send_long_dsp(message: Message,
                        state: FSMContext,
                        bot: Bot):
    data = await state.get_data()
    vacancy = Vacancy(id=data["id"])
    await vac_commands.edit_vacancy_data(vacancy, message.text, "s_dscr")
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)
    await message.answer(text=texts.edit_employer)
    await send_edited_vacancy(message, state)
    await state.clear()


@router.message(StateFilter(vfs.edit_long_dsp), F.text)
async def confirm_vacancy(message: Message,
                          state: FSMContext,
                          bot: Bot):
    data = await state.get_data()
    vacancy = Vacancy(id=data["id"])
    await vac_commands.edit_vacancy_data(vacancy, message.text, "l_dscr")
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)
    await message.answer(text=texts.edit_employer)
    await send_edited_vacancy(message, state)
    await state.clear()


@router.message(StateFilter(vfs.edit_image), F.photo | F.document)
async def confirm_vacancy(message: Message,
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

    path = f"{file_info.file_id}.{extension}"
    await bot.download_file(file_info.file_path, path)

    await vac_commands.save_image(path)
    image_id = await db_commands.get_last_insert_rowid()

    data = await state.get_data()
    vacancy = Vacancy(id=data["id"])

    await vac_commands.edit_vacancy_data(vacancy, image_id, "image_id")
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)
    await message.answer(text=texts.edit_image)
    await send_edited_vacancy(message, state)
    await state.clear()
