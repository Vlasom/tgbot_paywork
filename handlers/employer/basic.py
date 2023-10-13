from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from keyboards.inline_keyboards import *

from assets import texts
from classes import *

from fsm.statesform import StapesForm as sf

router = Router()


@router.callback_query(StateFilter(default_state), F.data.startswith("contact"))
async def callback_create_application(callback: CallbackQuery, state: FSMContext, user: User):
    vacancy = Vacancy(id=int(callback.data.split("_")[1]))

    if not await vac_commands.check_vacancy_application(user, vacancy):
        await state.update_data(vacancy_id=vacancy.id)
        await state.set_state(sf.create_application)
        await callback.message.answer(texts.creating_vacancy_application)
    else:
        await callback.message.answer(texts.not_save_application)
    await callback.answer()


@router.callback_query(F.data.startswith("created_more"))
async def callback_more_vacancy(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[2]))

    text = await vac_commands.to_text(vacancy=vacancy,
                                      type_descr="long")

    await callback.message.edit_text(text=text,
                                     reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                 btn_more_less="less"))


@router.callback_query(F.data.startswith("created_less"))
async def callback_less_vacancy(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[2]))

    text = await vac_commands.to_text(vacancy=vacancy,
                                      type_descr="short")

    await callback.message.edit_text(text=text, reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                            btn_more_less="more"))


@router.callback_query(StateFilter(default_state), F.data.startswith("edit_my"))
async def callback_my_edit(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[2]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[2][0].callback_data.split("_")[1]

    await callback.message.edit_reply_markup(reply_markup=await create_inkb_for_editing(id=vacancy.id,
                                                                                        btn_more_less=btn_more_less))


@router.callback_query(StateFilter(default_state), F.data.startswith("delete"))
async def callback_my_edit(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[1]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[2][0].callback_data.split("_")[1]
    print(callback.message.reply_markup.inline_keyboard[2][0].callback_data)
    print(callback.message.reply_markup.inline_keyboard[2][0])
    print(callback.message.reply_markup.inline_keyboard)

    await callback.message.edit_reply_markup(reply_markup=await create_inkb_for_deleting(id=vacancy.id,
                                                                                         btn_more_less=btn_more_less))


@router.callback_query(StateFilter(default_state), F.data.startswith("confirm_del"))
async def callback_my_edit(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[2]))
    await vac_commands.delete_vacancy(vacancy)
    await callback.message.edit_text(texts.delete_vacancy)


@router.callback_query(StateFilter(default_state), F.data.startswith("my_back_editing"))
async def callback_my_edit(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[9][0].callback_data.split("_")[1]
    await callback.message.edit_reply_markup(reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                         btn_more_less=btn_more_less))


@router.callback_query(StateFilter(default_state), F.data.startswith("my_back_deleting"))
async def callback_my_edit(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[1][0].callback_data.split("_")[1]
    await callback.message.edit_reply_markup(reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                         btn_more_less=btn_more_less))


@router.callback_query(StateFilter(default_state), F.data.startswith("editing_more"))
async def callback_my_edit(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[2]))
    btn_more_less = "less"

    text = await vac_commands.to_text(vacancy=vacancy,
                                      type_descr="long")

    await callback.message.edit_text(text=text, reply_markup=await create_inkb_for_editing(id=vacancy.id,
                                                                                           btn_more_less=btn_more_less))


@router.callback_query(StateFilter(default_state), F.data.startswith("editing_less"))
async def callback_my_edit(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[2]))
    btn_more_less = "more"

    text = await vac_commands.to_text(vacancy=vacancy,
                                      type_descr="short")

    await callback.message.edit_text(text=text, reply_markup=await create_inkb_for_editing(id=vacancy.id,
                                                                                           btn_more_less=btn_more_less))


@router.callback_query(StateFilter(default_state), F.data.startswith("deleting_more"))
async def callback_my_edit(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[2]))
    btn_more_less = "less"

    text = await vac_commands.to_text(vacancy=vacancy,
                                      type_descr="long")

    await callback.message.edit_text(text=text, reply_markup=await create_inkb_for_deleting(id=vacancy.id,
                                                                                            btn_more_less=btn_more_less))


@router.callback_query(StateFilter(default_state), F.data.startswith("deleting_less"))
async def callback_my_edit(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[2]))
    btn_more_less = "more"

    text = await vac_commands.to_text(vacancy=vacancy,
                                      type_descr="short")

    await callback.message.edit_text(text=text, reply_markup=await create_inkb_for_deleting(id=vacancy.id,
                                                                                            btn_more_less=btn_more_less))
