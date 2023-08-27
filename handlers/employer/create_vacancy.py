import asyncio
import pprint as p
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from fsm.statesform import StapesForm as sf
from assets import texts
from aiogram import Router, Bot, F
from aiogram.filters import Command, Text, StateFilter

from keyboard.inline_keyboards import *


router = Router()


@router.message(~StateFilter(default_state), Command(commands=['cancel']))
async def command_cancel_create(message: Message):
    await message.answer(text=texts.sure_cancel_create_vacancy,
                         reply_markup=inkb_yes_no)


@router.callback_query(Text("canceling"))
async def callback_canceling(callback: CallbackQuery,
                             state: FSMContext,
                             bot: Bot):
    try:
        await bot.delete_message(chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id - 1)

        await bot.delete_message(chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id - 2)
    except Exception as ex:
        pass

    await bot.edit_message_text(text=texts.cancel_create_vacancy,
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id)

    await callback.message.answer(text=texts.main_text())
    await state.clear()


@router.callback_query(Text("employer"))
async def callback_sent_employer(callback: CallbackQuery,
                                 state: FSMContext):
    await callback.message.edit_text(text=f"{texts.employ_or_employer}\n———\nСоздание заявки")
    await callback.message.answer(text=texts.start_create)
    await callback.message.answer(text=texts.fill_employer)
    await state.set_state(sf.fill_employer)


@router.message(StateFilter(sf.fill_employer), F.text)
async def sent_job(message: Message,
                   state: FSMContext,
                   bot: Bot):

    await state.set_state(sf.fill_job)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"Указанная организация:\n———\n_*{message.text}*_",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id,
                                parse_mode="MarkdownV2")

    await message.delete()

    await message.answer(text=texts.fill_job)
    await state.update_data(employer=message.text)


@router.message(StateFilter(sf.fill_job), F.text)
async def sent_salary(message: Message,
                      state: FSMContext,
                      bot: Bot):

    await state.set_state(sf.fill_salary)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"Указанная необходимая должность:\n———\n_*{message.text}*_",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id,
                                parse_mode="MarkdownV2")

    await message.delete()

    await message.answer(text=texts.fill_salary)
    await state.update_data(job=message.text)


@router.message(StateFilter(sf.fill_salary), F.text)
async def sent_minage(message: Message,
                      state: FSMContext,
                      bot: Bot):

    await state.set_state(sf.fill_minage)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"Указанная заработная плату:\n———\n_*{message.text}*_",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id,
                                parse_mode="MarkdownV2")

    await message.delete()

    await message.answer(text=texts.fill_minage,
                         reply_markup=inkb_skip_stage_create)

    await state.update_data(salary=message.text)


@router.message(StateFilter(sf.fill_minage), F.text)
async def sent_minexp(message: Message,
                      state: FSMContext,
                      bot: Bot):

    await state.set_state(sf.fill_minexp)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"Указанный минимальный допустимый возраст:\n———\n_*{message.text}*_",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id,
                                parse_mode="MarkdownV2")
    await message.delete()

    await message.answer(text=texts.fill_minexp,
                         reply_markup=inkb_skip_stage_create)

    await state.update_data(minage=message.text)


@router.message(StateFilter(sf.fill_minexp), F.text)
async def sent_date(message: Message,
                    state: FSMContext,
                    bot: Bot):

    await state.set_state(sf.fill_date)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"Указанный минимальный опыт работы:\n———\n_*{message.text}*_",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id,
                                parse_mode="MarkdownV2")

    await message.delete()

    await message.answer(text=texts.fill_date)
    await state.update_data(minexp=message.text)


@router.message(StateFilter(sf.fill_date), F.text)
async def sent_short_dsp(message: Message,
                         state: FSMContext,
                         bot: Bot):

    await state.set_state(sf.fill_short_dsp)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"Указанное время или период работы вакансии:\n———\n_*{message.text}*_",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id,
                                parse_mode="MarkdownV2")
    await message.delete()

    await message.answer(text=texts.fill_short_dsp)
    await state.update_data(date=message.text)


@router.message(StateFilter(sf.fill_short_dsp), F.text)
async def sent_long_dsp(message: Message,
                        state: FSMContext,
                        bot: Bot):

    await state.set_state(sf.fill_long_dsp)

    message_to_edit_id = message.message_id - 1
    await bot.edit_message_text(text=f"Указанное краткое описание вакансии:\n———\n_*{message.text}*_",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id,
                                parse_mode="MarkdownV2")

    await message.delete()

    await message.answer(text=texts.fill_long_dsp)
    await state.update_data(short_dsp=message.text)


@router.message(StateFilter(sf.fill_long_dsp), F.text)
async def confirm_vacancy(message: Message,
                          state: FSMContext,
                          bot: Bot):

    await state.set_state(sf.confirm_create)

    message_to_edit_id = message.message_id - 1

    words: list = message.text.split(" ")
    answer: str = " ".join([word for word in words[:10]])
    await bot.edit_message_text(text=f"Указанное длинное описание:\n———\n<i><b>{answer}"
                                     f"{'...' if len(words) > 10 else ''}</b></i>",
                                chat_id=message.from_user.id,
                                message_id=message_to_edit_id,
                                parse_mode="HTML")

    await state.update_data(long_dsp=message.text)
    await message.answer(text=texts.confirm_vacancy)

    data = await state.get_data()
    await message.answer(text=texts.confirm_vacancy_txt(data, type_descr="short"),
                         reply_markup=inkb_contact_like_more,
                         parse_mode="MarkdownV2")
    await message.delete()

    # сохранение данных и что-то ещё
    await asyncio.sleep(0.5)
    await message.answer(text=texts.mess12dsh,
                         reply_markup=inkb_edit_cancel_save)


@router.callback_query(StateFilter(sf.confirm_create), Text("skip_stage_create"))
async def callback_skip_stage_create_vacancy(callback: CallbackQuery):

    await callback.message.edit_text(text=texts.sure_cancel_create_vacancy,
                                     reply_markup=inkb_yes_no)


@router.callback_query(StateFilter(sf.confirm_create), Text("vacancy_cancel"))
async def callback_cancel_create_vacancy(callback: CallbackQuery):

    await callback.message.edit_text(text=texts.sure_cancel_create_vacancy,
                                     reply_markup=inkb_yes_no)


@router.callback_query(StateFilter(sf.confirm_create), Text("vacancy_save"))
async def callback_save_create_vacancy(callback: CallbackQuery,
                                       state: FSMContext,
                                       bot: Bot):
    # Сохранение в БД
    await callback.message.edit_text(text="Вакансия сохранена")

    try:
        await bot.delete_message(chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id - 1)

        await bot.delete_message(chat_id=callback.from_user.id,
                                 message_id=callback.message.message_id - 2)
    except Exception as ex:
        pass

    await callback.message.answer(text=texts.main_text())
    await state.clear()


@router.callback_query(StateFilter(sf.confirm_create), Text("vacancy_edit"))
async def callback_edit_create_vacancy(callback: CallbackQuery):
    await callback.message.edit_text(text="Выберите, что вы хотите отредактировать",
                                     reply_markup=inkb_edit_vac)


@router.callback_query(StateFilter(sf.confirm_create), Text("back"))
async def callback_edit_create_vacancy_back(callback: CallbackQuery):
    await callback.message.edit_text(text="Что вы хотите сделать?",
                                     reply_markup=inkb_edit_cancel_save)


@router.callback_query(StateFilter(sf.confirm_create), Text("more"))
async def callback_more_vacancy(callback: CallbackQuery,
                                state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(text=texts.confirm_vacancy_txt(data, type_descr="long"),
                                     reply_markup=inkb_contact_like_less,
                                     parse_mode="MarkdownV2")


@router.callback_query(StateFilter(sf.confirm_create), Text("less"))
async def callback_less_vacancy(callback: CallbackQuery,
                                state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(text=texts.confirm_vacancy_txt(data, type_descr="short"),
                                     reply_markup=inkb_contact_like_more,
                                     parse_mode="MarkdownV2")


@router.callback_query(StateFilter(sf.confirm_create), Text("like"))
async def callback_like_vacancy(callback: CallbackQuery):
    await callback.answer(text="Сейчас вы создаете вакансию, но в ином случае вы могли бы сохранить данную вакансию в избранные",
                          show_alert=True)


@router.callback_query(StateFilter(sf.confirm_create), Text("contact"))
async def callback_contact_vacancy(callback: CallbackQuery):
    await callback.answer(text="Сейчас вы создаете вакансию, но в ином случае вы могли бы оставить заяку",
                          show_alert=True)
