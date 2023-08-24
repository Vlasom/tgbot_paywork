from tgbot import *
from assets import texts
from vacancy import VacanciesEmploy


async def callback_employ_vacancies(callback: types.CallbackQuery):
    await callback.message.answer(texts.employ_warn_info)

    await callback.message.answer(texts.employ_warn_info)

    queue = QueueVacancy(user_id=callback.message.from_user.id)

    vacancy = VacanciesEmploy("asd")

    text = str(vacancy.get_db_row())

    await callback.message.answer(text)


async def callback_next_vacancy(callback: types.CallbackQuery):

    markup = InlineKeyboardMarkup(inline_keyboard=[[
        inline_buttons.btn_more,
        inline_buttons.btn_like],
        [inline_buttons.btn_next]])
    message_text = "sfd"
    await callback.message.answer(message_text, reply_markup=markup)

    markup = InlineKeyboardMarkup(inline_keyboard=[[
        inline_buttons.btn_more,
        inline_buttons.btn_like]])
    await callback.message.edit_reply_markup(reply_markup=markup)


async def callback_more_vacancy(callback: types.CallbackQuery):

    if inline_buttons.btn_next in callback.message.reply_markup.inline_keyboard[-1]:
        markup = InlineKeyboardMarkup(inline_keyboard=[[
            inline_buttons.btn_less,
            inline_buttons.btn_like],
            [inline_buttons.btn_next]])
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[[
            inline_buttons.btn_less,
            inline_buttons.btn_like]])

    await callback.message.edit_text("очко", reply_markup=markup)


async def callback_less_vacancy(callback: types.CallbackQuery):
    message_text = "sfd"
    btn_next = InlineKeyboardButton(text='Следующаю', callback_data='next')
    btn_more = InlineKeyboardButton(text='Подробнее', callback_data='more')
    btn_like = InlineKeyboardButton(text='В избранное', callback_data='like')
    markup = InlineKeyboardMarkup(inline_keyboard=[[btn_next, btn_more, btn_like]])

    await callback.message.answer(message_text, reply_markup=markup)


async def callback_like_vacancy(callback: types.CallbackQuery):
    message_text = "sfd"
    btn_next = InlineKeyboardButton(text='Следующаю', callback_data='next')
    btn_more = InlineKeyboardButton(text='Подробнее', callback_data='more')
    btn_like = InlineKeyboardButton(text='В избранное', callback_data='like')
    markup = InlineKeyboardMarkup(inline_keyboard=[[btn_next, btn_more, btn_like]])

    await callback.message.answer(message_text, reply_markup=markup)