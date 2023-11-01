import asyncio

from aiogram.types import Message, CallbackQuery, FSInputFile, ContentType
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter

from classes.Statesform import VacancyFormSteps as vfs
from keyboards.inline_keyboards import *

from ..employer import edit_vacancy
from classes import *
from assets import texts
from utils.setcomands import set_cancel_create_command, set_default_commands

router = Router()
router.include_router(edit_vacancy.router)


@router.message(StateFilter(vfs.fill_employer, vfs.fill_job, vfs.fill_salary, vfs.fill_min_age,
                            vfs.fill_min_exp, vfs.fill_date, vfs.fill_short_dsp, vfs.fill_long_dsp, vfs.confirm_create),
                Command(commands=['cancel']))
async def command_cancel_create(message: Message):
    await message.answer(text=texts.sure_cancel_create_vacancy,
                         reply_markup=inkb_yes_no)


@router.callback_query(F.data == "continue")
async def callback_canceling(callback: CallbackQuery,
                             state: FSMContext,
                             bot: Bot):
    await callback.message.delete()
    await bot.delete_message(chat_id=callback.from_user.id,
                             message_id=callback.message.message_id - 1)

    # если не отправлять новое сообщение то телеграм не сможет найти сообщение для редактирования
    state_now = await state.get_state()
    if state_now == vfs.fill_employer:
        await callback.message.answer(texts.fill_employer)
    if state_now == vfs.fill_job:
        await callback.message.answer(texts.fill_job)
    if state_now == vfs.fill_salary:
        await callback.message.answer(texts.fill_salary)
    if state_now == vfs.fill_min_age:
        await callback.message.answer(texts.fill_min_age, reply_markup=inkb_skip_stage_create)
    if state_now == vfs.fill_min_exp:
        await callback.message.answer(texts.fill_min_exp, reply_markup=inkb_skip_stage_create)
    if state_now == vfs.fill_short_dsp:
        await callback.message.answer(texts.fill_date)
    if state_now == vfs.fill_long_dsp:
        await callback.message.answer(texts.fill_short_dsp)
    if state_now == vfs.fill_image:
        await callback.message.answer(texts.fill_image)


@router.callback_query(F.data == "canceling")
async def callback_canceling(callback: CallbackQuery,
                             state: FSMContext,
                             user: User,
                             bot: Bot):
    await bot.delete_message(chat_id=callback.from_user.id,
                             message_id=callback.message.message_id - 1)
    await bot.delete_message(chat_id=callback.from_user.id,
                             message_id=callback.message.message_id - 2)

    await bot.edit_message_text(text=texts.cancel_create_vacancy,
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id)
    await set_default_commands(bot, callback.from_user.id)
    markup = inkb_verified_users if await redis_commands.check_verification(user) else inkb_not_verified_users
    await callback.message.answer(text=texts.main_page, reply_markup=markup)
    await state.clear()


@router.callback_query(F.data == "employer")
async def callback_send_employer(callback: CallbackQuery,
                                 state: FSMContext,
                                 bot: Bot):
    await callback.message.edit_text(text=f"{texts.employ_or_employer}\n———\nСоздание заявки")
    await callback.message.answer(text=texts.start_create)
    await callback.message.answer(text=texts.fill_employer)
    await set_cancel_create_command(bot, callback.from_user.id)
    await state.set_state(vfs.fill_employer)


@router.message(StateFilter(vfs.fill_employer), F.text)
async def send_job(message: Message,
                   state: FSMContext,
                   bot: Bot):
    await state.set_state(vfs.fill_job)
    await state.update_data(employer=message.text)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"Указанная организация:\n———\n<b><i>{message.text}</i></b>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)

    await message.delete()

    await message.answer(text=texts.fill_job)


@router.message(StateFilter(vfs.fill_job), F.text)
async def send_salary(message: Message,
                      state: FSMContext,
                      bot: Bot):
    await state.set_state(vfs.fill_salary)
    await state.update_data(work_type=message.text)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"Указанная необходимая должность:\n———\n<b><i>{message.text}</i></b>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)

    await message.delete()

    await message.answer(text=texts.fill_salary)


@router.message(StateFilter(vfs.fill_salary), F.text)
async def send_min_age(message: Message,
                       state: FSMContext,
                       bot: Bot):
    await state.set_state(vfs.fill_min_age)
    await state.update_data(salary=message.text)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"Указанная заработная плату:\n———\n<b><i>{message.text}</i></b>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)

    await message.delete()

    await message.answer(text=texts.fill_min_age,
                         reply_markup=inkb_skip_stage_create)


@router.message(StateFilter(vfs.fill_min_age), F.text)
async def send_min_exp(message: Message,
                       state: FSMContext,
                       bot: Bot):
    await state.set_state(vfs.fill_min_exp)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"Указанный минимальный допустимый возраст:\n———\n<b><i>{message.text}</i></b>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)
    await message.delete()

    await message.answer(text=texts.fill_min_exp,
                         reply_markup=inkb_skip_stage_create)

    await state.update_data(min_age=message.text)


@router.message(StateFilter(vfs.fill_min_exp), F.text)
async def send_date(message: Message,
                    state: FSMContext,
                    bot: Bot):
    await state.set_state(vfs.fill_date)
    await state.update_data(min_exp=message.text)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"Указанный минимальный опыт работы:\n———\n<b><i>{message.text}</i></b>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)

    await message.delete()

    await message.answer(text=texts.fill_date)


@router.message(StateFilter(vfs.fill_date), F.text)
async def send_short_dsp(message: Message,
                         state: FSMContext,
                         bot: Bot):
    await state.set_state(vfs.fill_short_dsp)
    await state.update_data(datetime=message.text)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"Указанное время или период работы вакансии:\n———\n<b><i>{message.text}</i></b>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)
    await message.delete()

    await message.answer(text=texts.fill_short_dsp)


@router.message(StateFilter(vfs.fill_short_dsp), F.text)
async def send_long_dsp(message: Message,
                        state: FSMContext,
                        bot: Bot):
    await state.set_state(vfs.fill_long_dsp)
    await state.update_data(s_dscr=message.text)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"Указанное краткое описание вакансии:\n———\n<b><i>{message.text}</i></b>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)

    await message.delete()

    await message.answer(text=texts.fill_long_dsp)


@router.message(StateFilter(vfs.fill_long_dsp), F.text)
async def send_image(message: Message,
                     state: FSMContext,
                     bot: Bot):
    await state.set_state(vfs.fill_image)
    await state.update_data(l_dscr=message.text)

    message_to_edit_id = message.message_id - 1

    words: list = message.text.split(" ")
    answer: str = " ".join([word for word in words[:10]])

    await bot.edit_message_text(text=f"Указанное длинное описание:\n———\n<i><b>{answer}"
                                     f"{'...' if len(words) > 10 else ''}</b></i>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id)

    await message.delete()

    photo = FSInputFile(path="default_image.jpg")
    await message.answer_photo(photo=photo, caption=texts.fill_image, reply_markup=inkb_skip_stage_create)


@router.message(StateFilter(vfs.fill_image), F.photo | F.document)
async def confirm_create(message: Message, state: FSMContext, bot: Bot):
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
    await state.update_data(image=path)

    await message.answer(text=texts.confirm_vacancy)

    data = await state.get_data()
    photo = FSInputFile(path=path)
    await message.answer_photo(photo=photo,
                               caption=await db_commands.dict_to_text(vacancy_values=data,
                                                                      type_descr="short"),
                               reply_markup=inkb_preview_more)

    await asyncio.sleep(0.3)
    await message.answer(text=texts.mess12dsh,
                         reply_markup=inkb_edit_cancel_save)
    await state.set_state(vfs.confirm_create)


@router.callback_query(StateFilter(vfs.fill_min_age), F.data == "skip_stage_create")
async def callback_skip_min_age_create_vacancy(callback: CallbackQuery, state: FSMContext):
    await state.set_state(vfs.fill_min_exp)
    await state.update_data(min_age=None)
    await callback.message.edit_text(text=f"Указанный минимальный допустимый возраст:\n———\nПропущено")
    await callback.message.answer(text=texts.fill_min_exp,
                                  reply_markup=inkb_skip_stage_create)


@router.callback_query(StateFilter(vfs.fill_min_exp), F.data == "skip_stage_create")
async def callback_skip_min_exp_create_vacancy(callback: CallbackQuery, state: FSMContext):
    await state.set_state(vfs.fill_date)
    await state.update_data(min_exp=None)
    await callback.message.edit_text(text=f"Указанное краткое описание вакансии:\n———\nПропущено")
    await callback.message.answer(text=texts.fill_date)


@router.callback_query(StateFilter(vfs.fill_image), F.data == "skip_stage_create")
async def callback_skip_min_exp_create_vacancy(callback: CallbackQuery, state: FSMContext):
    await state.set_state(vfs.confirm_create)
    await state.update_data(image="0")
    await callback.message.edit_caption(
        caption=f"Это изображение по умолчанию, вы можете его изменить\n———\nПропущено")

    await callback.message.answer(text=texts.confirm_vacancy)

    data = await state.get_data()
    photo = FSInputFile(path="default_image.jpg")
    await callback.message.answer_photo(photo=photo,
                                        caption=await db_commands.dict_to_text(vacancy_values=data,
                                                                               type_descr="short"),
                                        reply_markup=inkb_preview_more)

    await asyncio.sleep(0.3)
    await callback.message.answer(text=texts.mess12dsh,
                                  reply_markup=inkb_edit_cancel_save)


@router.callback_query(StateFilter(vfs.confirm_create), F.data == "vacancy_cancel")
async def callback_cancel_create_vacancy(callback: CallbackQuery):
    await callback.message.edit_text(text=texts.sure_cancel_create_vacancy,
                                     reply_markup=inkb_back_yes)


@router.callback_query(StateFilter(vfs.confirm_create), F.data == "vacancy_save")
async def callback_save_create_vacancy(callback: CallbackQuery,
                                       state: FSMContext,
                                       bot: Bot,
                                       user: User):
    await state.update_data(creator_id=callback.from_user.id)

    data = await state.get_data()

    if (path := data.get("image")) != "0":
        await vac_commands.save_image(path)
        data["image"] = await db_commands.get_last_insert_rowid()

    vacancy_text = await db_commands.dict_to_text(vacancy_values=data, type_descr="short")
    vacancy = Vacancy(id=-1, values=data, text=vacancy_text)
    await vac_commands.create(vacancy)
    vacancy.id = await db_commands.get_last_insert_rowid()

    await callback.message.edit_text(text="Вакансия сохранена")

    # notif_sender = NotificationsSender(text="Появилась новая ваканчия:\n\n" + vacancy.text,
    #                                    markup=await create_inkb_for_employ(id=created_vacancy_id, is_next=False,
    #                                                                        btn_like_nlike="like",
    #                                                                        btn_more_less="more"),
    #                                    db_notification=vac_notification,
    #                                    notification_name=f"vacancy_notifi_{vacancy.id}",
    #                                    creator=user,
    #                                    bot=bot)
    #
    # await notif_sender.sender(is_vacancy_notification=True)

    await bot.delete_message(chat_id=callback.from_user.id,
                             message_id=callback.message.message_id - 1)
    await bot.delete_message(chat_id=callback.from_user.id,
                             message_id=callback.message.message_id - 2)

    markup = inkb_verified_users if await redis_commands.check_verification(user) else inkb_not_verified_users
    await callback.message.answer(text=texts.main_page, reply_markup=markup)
    await set_default_commands(bot, callback.from_user.id)

    await state.clear()


@router.callback_query(StateFilter(vfs.confirm_create), F.data == "vacancy_edit")
async def callback_edit_create_vacancy(callback: CallbackQuery):
    await callback.message.edit_text(text="Выберите, что вы хотите отредактировать",
                                     reply_markup=inkb_edit_vac)


@router.callback_query(StateFilter(vfs.confirm_create), F.data == "back")
async def callback_edit_create_vacancy_back(callback: CallbackQuery):
    await callback.message.edit_text(text="Что вы хотите сделать?",
                                     reply_markup=inkb_edit_cancel_save)


@router.callback_query(F.data == "preview_more")
async def callback_more_vacancy(callback: CallbackQuery,
                                state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_caption(caption=await db_commands.dict_to_text(vacancy_values=data,
                                                                               type_descr="long"),
                                        reply_markup=inkb_preview_less)


@router.callback_query(F.data == "preview_less")
async def callback_less_vacancy(callback: CallbackQuery,
                                state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_caption(caption=await db_commands.dict_to_text(vacancy_values=data,
                                                                               type_descr="short"),
                                        reply_markup=inkb_preview_more)


@router.callback_query(StateFilter(vfs.confirm_create), F.data == "preview_like")
async def callback_like_vacancy(callback: CallbackQuery):
    await callback.answer(
        text="Сейчас вы создаете вакансию, но в ином случае вы могли бы сохранить данную вакансию в избранные",
        show_alert=True)


@router.callback_query(StateFilter(vfs.confirm_create), F.data == "preview_contact")
async def callback_contact_vacancy(callback: CallbackQuery):
    await callback.answer(text="Сейчас вы создаете вакансию, но в ином случае вы могли бы оставить заяку",
                          show_alert=True)
