from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

_btn_employer = InlineKeyboardButton(text='Создать заявку 📝', callback_data='employer')
_btn_employ = InlineKeyboardButton(text='Смотреть вакансии 👀', callback_data='employ')

_btn_favorites = InlineKeyboardButton(text='Избранные ⭐️', callback_data='favorites')
_btn_my_vacancies = InlineKeyboardButton(text='Мои вакансии 📥', callback_data='my_vacancies')

_btn_contact = InlineKeyboardButton(text='Связаться 📞', callback_data='contact')
btn_next = InlineKeyboardButton(text='Следующаю ➡️', callback_data='next')
_btn_more = InlineKeyboardButton(text='Подробнее ⬇️', callback_data='more')
_btn_like = InlineKeyboardButton(text='В избранное ☆', callback_data='like')
_btn_less = InlineKeyboardButton(text='Свернуть ⬆️', callback_data='less')

_btn_view_responses = InlineKeyboardButton(text='Свернуть 📲', callback_data='responses')
_btn_v_responses = InlineKeyboardButton(text='Свернуть 📲', callback_data='responses')

_btn_on_notifi = InlineKeyboardButton(text='Да, буду ждать🔔', callback_data='on_notification')
_btn_off_notifi = InlineKeyboardButton(text='Нет, не нужно🔕', callback_data='off_notification')

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

inkb_mane_page = InlineKeyboardMarkup(inline_keyboard=[[_btn_employer],
                                                       [_btn_employ],
                                                       [_btn_favorites],
                                                       [_btn_my_vacancies]])

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

inkb_yes_back = InlineKeyboardMarkup(inline_keyboard=[[_btn_yes, _btn_back]])
inkb_yes_no = InlineKeyboardMarkup(inline_keyboard=[[_btn_yes, _btn_no]])

inkb_on_off_notifi = InlineKeyboardMarkup(inline_keyboard=[[_btn_on_notifi],
                                                           [_btn_off_notifi]])

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


async def create_inkb(id, is_next, btn_like_nlike, btn_more_less) -> InlineKeyboardMarkup:
    btn_contact = InlineKeyboardButton(text='Связаться 📞', callback_data=f'contact_{id}')
    btn_like = InlineKeyboardButton(text='В избранное ☆', callback_data=f'like_{id}')
    btn_nlike = InlineKeyboardButton(text='Из избранного ★', callback_data=f'nlike_{id}')
    btn_more = InlineKeyboardButton(text='Подробнее ⬇️', callback_data=f'more_{id}')
    btn_less = InlineKeyboardButton(text='Свернуть ⬆️', callback_data=f'less_{id}')
    btn_next = InlineKeyboardButton(text='Следующаю ➡️', callback_data=f'next_{id}')

    if btn_like_nlike == "like":
        btn_like_nlike = btn_like
    else:
        btn_like_nlike = btn_nlike

    if btn_more_less == "more":
        btn_more_less = btn_more
    else:
        btn_more_less = btn_less

    if not is_next:
        return InlineKeyboardMarkup(inline_keyboard=[[btn_contact, btn_like_nlike],
                                                     [btn_more_less]])
    if is_next:
        return InlineKeyboardMarkup(inline_keyboard=[[btn_contact, btn_more_less, btn_like_nlike],
                                                     [btn_next]])


async def create_inkb_for_employer(id, btn_more_less) -> InlineKeyboardMarkup:
    btn_delete = InlineKeyboardButton(text='Удалить 🗑', callback_data=f'del_{id}')
    btn_edit = InlineKeyboardButton(text='Редактировать ✏️', callback_data=f'edit_my_{id}')
    btn_applications = InlineKeyboardButton(text='Отклики 📲', callback_data=f'applications_{id}')

    btn_more = InlineKeyboardButton(text='Подробнее ⬇️', callback_data=f'created_more_{id}')
    btn_less = InlineKeyboardButton(text='Свернуть ⬆️', callback_data=f'created_less_{id}')

    if btn_more_less == "more":
        btn_more_less = btn_more
    else:
        btn_more_less = btn_less

    return InlineKeyboardMarkup(inline_keyboard=[[btn_delete, btn_edit],
                                                 [btn_applications],
                                                 [btn_more_less]])


async def create_inkb_for_editing(id, btn_more_less) -> InlineKeyboardMarkup:
    btn_edit_employer = InlineKeyboardButton(text='Организация 🏛', callback_data=f'my_edit_employer_{id}')
    btn_edit_job = InlineKeyboardButton(text='Должность 👷‍♂️', callback_data=f'my_edit_job_{id}')
    btn_edit_salary = InlineKeyboardButton(text='Зарплата 💵', callback_data=f'my_edit_salary')
    btn_edit_minage = InlineKeyboardButton(text='Минимальный возраст 👶', callback_data=f'my_edit_minage_{id}')
    btn_edit_minexp = InlineKeyboardButton(text='Минимальный опыт работы 🕓', callback_data=f'my_edit_minexp_{id}')
    btn_edit_date = InlineKeyboardButton(text='Время ⏱', callback_data=f'my_edit_date_{id}')
    btn_edit_short_dsp = InlineKeyboardButton(text='Краткое описание 📃', callback_data=f'my_edit_short_dsp_{id}')
    btn_edit_long_dsp = InlineKeyboardButton(text='Подробное описание 📄', callback_data=f'my_edit_long_dsp_{id}')
    btn_back = InlineKeyboardButton(text='Назад ⬅️', callback_data=f'my_back_{id}')

    btn_more = InlineKeyboardButton(text='Подробнее ⬇️', callback_data=f'my_more_{id}')
    btn_less = InlineKeyboardButton(text='Свернуть ⬆️', callback_data=f'my_less_{id}')

    if btn_more_less == "more":
        btn_more_less = btn_more
    else:
        btn_more_less = btn_less

    return InlineKeyboardMarkup(inline_keyboard=[[btn_edit_employer],
                                                 [btn_edit_job],
                                                 [btn_edit_salary],
                                                 [btn_edit_minage],
                                                 [btn_edit_minexp],
                                                 [btn_edit_date],
                                                 [btn_edit_short_dsp],
                                                 [btn_edit_long_dsp],
                                                 [btn_back],
                                                 [btn_more_less]])
