from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram import Router, F, Bot

from keyboards.inline_keyboards import *
from ..employer import edit_my_vacancy
from assets import texts
from classes import *

router = Router()
router.include_router(edit_my_vacancy.router)


@router.callback_query(StateFilter(default_state), F.data.startswith("my_delete"))
async def callback_my_delete(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[2]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[2][0].callback_data.split("_")[1]
    await callback.message.edit_reply_markup(reply_markup=await create_inkb_for_deleting(id=vacancy.id,
                                                                                         btn_more_less=btn_more_less))


@router.callback_query(StateFilter(default_state), F.data.startswith("back_my_deleting"))
async def callback_back_my_deleting(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[1][0].callback_data.split("_")[1]
    await callback.message.edit_reply_markup(reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                         btn_more_less=btn_more_less))


@router.callback_query(StateFilter(default_state), F.data.startswith("confirm_my_deleting"))
async def callback_confirm_my_deleting(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))
    await vac_commands.delete_vacancy(vacancy)
    await callback.message.delete()
    await callback.message.answer(texts.delete_vacancy + str(vacancy.id))


@router.callback_query(StateFilter(default_state), F.data.startswith("my_deleting_more"))
async def callback_my_deleting_more(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))

    text = await vac_commands.to_text(vacancy=vacancy,
                                      type_descr="long")

    await callback.message.edit_caption(caption=text, reply_markup=await create_inkb_for_deleting(id=vacancy.id,
                                                                                                  btn_more_less="less"))


@router.callback_query(StateFilter(default_state), F.data.startswith("my_deleting_less"))
async def callback_my_deleting_less(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))

    text = await vac_commands.to_text(vacancy=vacancy,
                                      type_descr="short")

    await callback.message.edit_caption(caption=text, reply_markup=await create_inkb_for_deleting(id=vacancy.id,
                                                                                                  btn_more_less="more"))


@router.callback_query(StateFilter(default_state), F.data.startswith("my_edit"))
async def callback_my_edit(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[2]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[2][0].callback_data.split("_")[1]

    await callback.message.edit_reply_markup(reply_markup=await create_inkb_for_editing(id=vacancy.id,
                                                                                        btn_more_less=btn_more_less))


@router.callback_query(StateFilter(default_state), F.data.startswith("back_my_editing"))
async def callback_back_my_editing(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[9][0].callback_data.split("_")[1]
    await callback.message.edit_reply_markup(reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                         btn_more_less=btn_more_less))


@router.callback_query(StateFilter(default_state), F.data.startswith("my_editing_more"))
async def callback_my_editing_more(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))

    text = await vac_commands.to_text(vacancy=vacancy,
                                      type_descr="long")

    await callback.message.edit_caption(caption=text,
                                        reply_markup=await create_inkb_for_editing(id=vacancy.id,
                                                                                   btn_more_less="less"))


@router.callback_query(StateFilter(default_state), F.data.startswith("my_editing_less"))
async def callback_my_editing_less(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))

    text = await vac_commands.to_text(vacancy=vacancy,
                                      type_descr="short")

    await callback.message.edit_caption(caption=text,
                                        reply_markup=await create_inkb_for_editing(id=vacancy.id,
                                                                                   btn_more_less="more"))


@router.callback_query(StateFilter(default_state), F.data.startswith("applications"))
async def callback_show_applications(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[1]))
    await callback.message.answer(f"✉️ Отклики на вакансию №{vacancy.id}")
    applications = await vac_commands.get_vacancy_applications(vacancy)
    if applications:
        for application in applications:
            text = await vac_commands.application_to_text(application)
            await callback.message.answer(text, reply_markup=await create_inkb_application(user_id=application[0],
                                                                                           vacancy_id=vacancy.id))
    else:
        await callback.message.answer(texts.no_vacancy_application)


@router.callback_query(StateFilter(default_state), F.data.startswith("decline_application"))
async def callback_decline_application(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.data.split("_")[2])
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))

    await vac_commands.application_decline(user_id=user_id, vacancy_id=vacancy.id)

    await bot.send_message(chat_id=user_id,
                           text="❌ Ваш отклик был отклонен\n\n" + callback.message.text.split('\n\n')[1])

    await callback.message.edit_text(callback.message.text + "\n—————\n❌ Отклонено")


@router.callback_query(StateFilter(default_state), F.data.startswith("confirm_application"))
async def callback_confirm_application(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.data.split("_")[2])
    vacancy = Vacancy(id=int(callback.data.split("_")[3]))

    await vac_commands.application_confirm(user_id=user_id, vacancy_id=vacancy.id)

    await bot.send_message(chat_id=user_id,
                           text="✅ Ваш отклик был принят\n\n" + callback.message.text.split('\n\n')[1])

    await callback.message.edit_text(callback.message.text + "\n—————\n✅ Принято")


@router.callback_query(F.data.startswith("my_more"))
async def callback_my_more(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[2]))

    text = await vac_commands.to_text(vacancy=vacancy,
                                      type_descr="long")

    await callback.message.edit_caption(caption=text,
                                        reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                    btn_more_less="less"))


@router.callback_query(F.data.startswith("my_less"))
async def callback_my_less(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[2]))

    text = await vac_commands.to_text(vacancy=vacancy,
                                      type_descr="short")

    await callback.message.edit_caption(caption=text,
                                        reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                    btn_more_less="more"))
