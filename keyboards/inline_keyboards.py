from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

_btn_employer = InlineKeyboardButton(text='Создать заявку 📝', callback_data='employer')
_btn_employ = InlineKeyboardButton(text='Смотреть вакансии 👀', callback_data='employ')

_btn_contact = InlineKeyboardButton(text='Связаться 📞', callback_data='contact')
btn_next = InlineKeyboardButton(text='Следующаю ➡️', callback_data='next')
_btn_more = InlineKeyboardButton(text='Подробнее ⬇️', callback_data='more')
_btn_like = InlineKeyboardButton(text='В избранное ☆', callback_data='like')
_btn_less = InlineKeyboardButton(text='Свернуть ⬆️', callback_data='less')

_btn_yes = InlineKeyboardButton(text='Да ✅', callback_data='canceling')
_btn_no = InlineKeyboardButton(text='Нет ❌', callback_data='continue')

_btn_edit_employer = InlineKeyboardButton(text='Организация 🏛', callback_data='edit_employer')
_btn_edit_job = InlineKeyboardButton(text='Должность 👷‍♂️', callback_data='edit_job')
_btn_edit_salary = InlineKeyboardButton(text='Зарплата 💵', callback_data='edit_salary')
_btn_edit_minage = InlineKeyboardButton(text='Минимальный возраст 👶', callback_data='edit_minage')
_btn_edit_minexp = InlineKeyboardButton(text='Минимальный опыт работы 🕓', callback_data='edit_minexp')
_btn_edit_date = InlineKeyboardButton(text='Время ⏱', callback_data='edit_date')
_btn_edit_short_dsp = InlineKeyboardButton(text='Краткое описание 📃', callback_data='edit_short_dsp')
_btn_edit_long_dsp = InlineKeyboardButton(text='Подробное описание 📄', callback_data='edit_long_dsp')

_btn_cancel = InlineKeyboardButton(text='Отменить ❌', callback_data='vacancy_cancel')
_btn_save = InlineKeyboardButton(text='Сохранить ✅', callback_data='vacancy_save')
_btn_edit = InlineKeyboardButton(text='Редактировать ✏️', callback_data='vacancy_edit')
_btn_back = InlineKeyboardButton(text='Назад ⬅️', callback_data='back')
_btn_stop_edit = InlineKeyboardButton(text='Завершить изменения 🆗', callback_data='stop_edit')

inkb_skip_stage_create = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Пропустить ⏩', callback_data='skip_stage_create')]])

inkb_employ_employer = InlineKeyboardMarkup(inline_keyboard=[[
    _btn_employer,
    _btn_employ]])

inkb_contact_like_more_next = InlineKeyboardMarkup(inline_keyboard=[[
    _btn_contact, _btn_more,
    _btn_like],
    [btn_next]])

inkb_contact_like_more = InlineKeyboardMarkup(inline_keyboard=[[
    _btn_contact, _btn_like],
    [_btn_more]])

inkb_contact_like_less_next = InlineKeyboardMarkup(inline_keyboard=[[
    _btn_contact, _btn_less,
    _btn_like],
    [btn_next]])

inkb_contact_like_less = InlineKeyboardMarkup(inline_keyboard=[[_btn_contact, _btn_like],
                                                               [_btn_less]])

inkb_yes_no = InlineKeyboardMarkup(inline_keyboard=[[_btn_yes, _btn_back]])

inkb_edit_vac = InlineKeyboardMarkup(inline_keyboard=[[_btn_edit_employer],
                                                      [_btn_edit_job],
                                                      [_btn_edit_salary],
                                                      [_btn_edit_minage],
                                                      [_btn_edit_minexp],
                                                      [_btn_edit_date],
                                                      [_btn_edit_short_dsp],
                                                      [_btn_edit_long_dsp],
                                                      [_btn_back]])

inkb_process_edit_vac = InlineKeyboardMarkup(inline_keyboard=[[_btn_edit_employer],
                                                              [_btn_edit_job],
                                                              [_btn_edit_salary],
                                                              [_btn_edit_minage],
                                                              [_btn_edit_minexp],
                                                              [_btn_edit_date],
                                                              [_btn_edit_short_dsp],
                                                              [_btn_edit_long_dsp],
                                                              [_btn_stop_edit]])

inkb_edit_cancel_save = InlineKeyboardMarkup(inline_keyboard=[[_btn_edit],
                                                              [_btn_cancel, _btn_save]])


async def create_inkb(id, isnext, more_less) -> InlineKeyboardMarkup:
    btn_contact = InlineKeyboardButton(text='Связаться 📞', callback_data=f'contact_{id}')
    btn_like = InlineKeyboardButton(text='В избранное ☆', callback_data=f'like_{id}')
    btn_next = InlineKeyboardButton(text='Следующаю ➡️', callback_data=f'next_{id}')
    btn_more = InlineKeyboardButton(text='Подробнее ⬇️', callback_data=f'more_{id}')
    btn_less = InlineKeyboardButton(text='Свернуть ⬆️', callback_data=f'less_{id}')

    if not isnext:
        if more_less == "more":
            return InlineKeyboardMarkup(inline_keyboard=[[btn_contact, btn_like],
                                                         [btn_more]])
        if more_less == "less":
            return InlineKeyboardMarkup(inline_keyboard=[[btn_contact, btn_like],
                                                         [btn_less]])
    if isnext:
        if more_less == "more":
            return InlineKeyboardMarkup(inline_keyboard=[[btn_contact, btn_more, btn_like],
                                                         [btn_next]])
        if more_less == "less":
            return InlineKeyboardMarkup(inline_keyboard=[[btn_contact, btn_less, btn_like],
                                                         [btn_next]])
