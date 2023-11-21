from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

_btn_employer = InlineKeyboardButton(text='Создать вакансию 📝', callback_data='create_vacancy')
_btn_employ = InlineKeyboardButton(text='Смотреть вакансии 👀', callback_data='view_vacancies')

_btn_favorites = InlineKeyboardButton(text='Избранные ⭐️', callback_data='favorites')
_btn_my_vacancies = InlineKeyboardButton(text='Мои вакансии 🗂', callback_data='my_vacancies')
_btn_my_applications = InlineKeyboardButton(text='Мои отклики ✉️', callback_data='my_applications')

_btn_private_office = InlineKeyboardButton(text="Личный кабинет", callback_data="private_office")

_btn_delete_history = InlineKeyboardButton(text='Поcмотреть вакансии заново 🔄', callback_data='redisplay')
_btn_back_later = InlineKeyboardButton(text='Вернусь позже 🔜', callback_data='back_later')

_btn_on_notifi = InlineKeyboardButton(text='Да, присылать уведомления 🔔', callback_data='on_notification')
_btn_off_notifi = InlineKeyboardButton(text='Нет, не нужно 🔕', callback_data='off_notification')

_btn_contact = InlineKeyboardButton(text='Откликнутся 🔔', callback_data='preview_create_application')
_btn_like = InlineKeyboardButton(text='В избранное ❤️', callback_data='preview_like')
_btn_more = InlineKeyboardButton(text='Подробнее ⬇️', callback_data='preview_more')
_btn_less = InlineKeyboardButton(text='Свернуть ⬆️', callback_data='preview_less')

_btn_yes = InlineKeyboardButton(text='Да ✅', callback_data='confirm_deleting')
_btn_no = InlineKeyboardButton(text='Нет ❌', callback_data='decline_deleting')

_btn_edit_employer = InlineKeyboardButton(text='Организация 🏛', callback_data='edit_employer')
_btn_edit_job = InlineKeyboardButton(text='Должность 👷‍♂️', callback_data='edit_job')
_btn_edit_salary = InlineKeyboardButton(text='Зарплата 💰', callback_data='edit_salary')
_btn_edit_minage = InlineKeyboardButton(text='Минимальный возраст 👶', callback_data='edit_minage')
_btn_edit_minexp = InlineKeyboardButton(text='Минимальный опыт работы 🧠', callback_data='edit_minexp')
_btn_edit_date = InlineKeyboardButton(text='Период работы 🕑', callback_data='edit_date')
_btn_edit_short_dsp = InlineKeyboardButton(text='Краткое описание 📃', callback_data='edit_short_dsp')
_btn_edit_long_dsp = InlineKeyboardButton(text='Подробное описание 📄', callback_data='edit_long_dsp')
_btn_edit_image = InlineKeyboardButton(text='Картинка 🌄', callback_data='edit_image')

_btn_edit = InlineKeyboardButton(text='Редактировать ✏️', callback_data='edit_created_vacancy')
_btn_cancel_create = InlineKeyboardButton(text='Удалить 🗑', callback_data='delete_created_vacancy')
_btn_save = InlineKeyboardButton(text='Сохранить 📥', callback_data='save_created_vacancy')

_btn_back = InlineKeyboardButton(text='Назад ⬅️', callback_data='back_created_vacancy')

_btn_cancel_action = InlineKeyboardButton(text='Отменить ↩️', callback_data='cancel_action')

_btn_admin_sender = InlineKeyboardButton(text='Рассылка', callback_data='admin_sender')

_btn_sender_with_btn = InlineKeyboardButton(text='Безусловно', callback_data='sender_with_btn')
_btn_sender_without_btn = InlineKeyboardButton(text='Это недопустимо', callback_data='sender_without_btn')

_btn_sender_with_image = InlineKeyboardButton(text='Конечно', callback_data='sender_with_image')
_btn_sender_without_image = InlineKeyboardButton(text='Не сегодня', callback_data='sender_without_image')

_btn_start_sender = InlineKeyboardButton(text='Исполняй', callback_data='start_sender')
_btn_cancel_sender = InlineKeyboardButton(text='Прервать', callback_data='cancel_sender')

######################

inkb_skip_stage_create = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Пропустить ⏩', callback_data='skip_stage_create')]])

inkb_cancel_action = InlineKeyboardMarkup(inline_keyboard=[[_btn_cancel_action]])

inkb_employ_employer = InlineKeyboardMarkup(inline_keyboard=[[_btn_employ],
                                                             [_btn_employer]])

inkb_verified_users = InlineKeyboardMarkup(inline_keyboard=[[_btn_private_office],
                                                            [_btn_employer],
                                                            [_btn_employ],
                                                            [_btn_favorites],
                                                            [_btn_my_vacancies],
                                                            [_btn_my_applications]])

inkb_not_verified_users = InlineKeyboardMarkup(inline_keyboard=[[_btn_private_office],
                                                                [_btn_employ],
                                                                [_btn_my_vacancies],
                                                                [_btn_favorites]])

###################

inkb_back_yes = InlineKeyboardMarkup(inline_keyboard=[[_btn_back, _btn_yes]])
inkb_yes_no = InlineKeyboardMarkup(inline_keyboard=[[_btn_yes, _btn_no]])

inkb_no_more_vacancies = InlineKeyboardMarkup(inline_keyboard=[[_btn_delete_history],
                                                               [_btn_back_later]])

inkb_on_off_notifi = InlineKeyboardMarkup(inline_keyboard=[[_btn_on_notifi],
                                                           [_btn_off_notifi]])
inkb_preview_more = InlineKeyboardMarkup(inline_keyboard=[[_btn_contact, _btn_like],
                                                          [_btn_more]])
inkb_preview_less = InlineKeyboardMarkup(inline_keyboard=[[_btn_contact, _btn_like],
                                                          [_btn_less]])

inkb_edit_vac = InlineKeyboardMarkup(inline_keyboard=[[_btn_edit_employer],
                                                      [_btn_edit_job],
                                                      [_btn_edit_salary],
                                                      [_btn_edit_minage],
                                                      [_btn_edit_minexp],
                                                      [_btn_edit_date],
                                                      [_btn_edit_short_dsp],
                                                      [_btn_edit_long_dsp],
                                                      [_btn_edit_image],
                                                      [_btn_back]])

inkb_edit_cancel_save = InlineKeyboardMarkup(inline_keyboard=[[_btn_edit],
                                                              [_btn_cancel_create, _btn_save]])

inkb_admin_panel = InlineKeyboardMarkup(inline_keyboard=[[_btn_admin_sender]])

inkb_sender_with_without_image = InlineKeyboardMarkup(inline_keyboard=[[_btn_sender_with_image],
                                                                       [_btn_sender_without_image]])

inkb_sender_with_without_btn = InlineKeyboardMarkup(inline_keyboard=[[_btn_sender_with_btn],
                                                                     [_btn_sender_without_btn]])

inkb_start_cancel_sender = InlineKeyboardMarkup(inline_keyboard=[[_btn_start_sender],
                                                                 [_btn_cancel_sender]])


async def create_inkb_for_employ(id, is_next, btn_like_nlike, btn_more_less) -> InlineKeyboardMarkup:
    btn_contact = InlineKeyboardButton(text='Откликнутся 🔔', callback_data=f'create_application_{id}')
    btn_like = InlineKeyboardButton(text='В избранное ⭐️', callback_data=f'like_{id}')
    btn_nlike = InlineKeyboardButton(text='В избранном ❇️', callback_data=f'nlike_{id}')
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
        return InlineKeyboardMarkup(inline_keyboard=[[btn_contact, btn_like_nlike],
                                                     [btn_more_less],
                                                     [btn_next]])


async def create_inkb_for_employer(id, btn_more_less) -> InlineKeyboardMarkup:
    btn_delete = InlineKeyboardButton(text='Удалить 🗑', callback_data=f'my_delete_{id}')
    btn_edit = InlineKeyboardButton(text='Редактировать ✏️', callback_data=f'my_edit_{id}')
    btn_applications = InlineKeyboardButton(text='Отклики 📲', callback_data=f'applications_{id}')

    btn_more = InlineKeyboardButton(text='Подробнее ⬇️', callback_data=f'my_more_{id}')
    btn_less = InlineKeyboardButton(text='Свернуть ⬆️', callback_data=f'my_less_{id}')

    if btn_more_less == "more":
        btn_more_less = btn_more
    else:
        btn_more_less = btn_less

    return InlineKeyboardMarkup(inline_keyboard=[[btn_delete, btn_edit],
                                                 [btn_applications],
                                                 [btn_more_less]])


async def create_inkb_for_editing(id, btn_more_less) -> InlineKeyboardMarkup:
    btn_edit_employer = InlineKeyboardButton(text='Организация 🏛', callback_data=f'edit_my_employer_{id}')
    btn_edit_job = InlineKeyboardButton(text='Должность 👷‍♂️', callback_data=f'edit_my_job_{id}')
    btn_edit_salary = InlineKeyboardButton(text='Зарплата 💵', callback_data=f'edit_my_salary')
    btn_edit_minage = InlineKeyboardButton(text='Минимальный возраст 👶', callback_data=f'edit_my_minage_{id}')
    btn_edit_minexp = InlineKeyboardButton(text='Минимальный опыт работы 🕓', callback_data=f'edit_my_minexp_{id}')
    btn_edit_date = InlineKeyboardButton(text='Время ⏱', callback_data=f'edit_my_date_{id}')
    btn_edit_short_dsp = InlineKeyboardButton(text='Краткое описание 📃', callback_data=f'edit_my_short_dsp_{id}')
    btn_edit_long_dsp = InlineKeyboardButton(text='Подробное описание 📄', callback_data=f'edit_my_long_dsp_{id}')
    btn_edit_image = InlineKeyboardButton(text='Картинка 🖼', callback_data=f'edit_my_image_{id}')
    btn_back = InlineKeyboardButton(text='Назад ⬅️', callback_data=f'back_my_editing_{id}')

    btn_more = InlineKeyboardButton(text='Подробнее ⬇️', callback_data=f'my_editing_more_{id}')
    btn_less = InlineKeyboardButton(text='Свернуть ⬆️', callback_data=f'my_editing_less_{id}')

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
                                                 [btn_edit_image],
                                                 [btn_back],
                                                 [btn_more_less]])


async def create_inkb_for_deleting(id, btn_more_less) -> InlineKeyboardMarkup:
    btn_back = InlineKeyboardButton(text='Назад ⬅️', callback_data=f'back_my_deleting_{id}')
    btn_yes = InlineKeyboardButton(text='Удалить ✅', callback_data=f'confirm_my_deleting_{id}')

    btn_more = InlineKeyboardButton(text='Подробнее ⬇️', callback_data=f'my_deleting_more_{id}')
    btn_less = InlineKeyboardButton(text='Свернуть ⬆️', callback_data=f'my_deleting_less_{id}')

    if btn_more_less == "more":
        btn_more_less = btn_more
    else:
        btn_more_less = btn_less

    return InlineKeyboardMarkup(inline_keyboard=[[btn_back, btn_yes],
                                                 [btn_more_less]])


async def create_inkb_application(user_id: int, vacancy_id: int) -> InlineKeyboardMarkup:
    btn_decline = InlineKeyboardButton(text='Отклонить ❌', callback_data=f'decline_application_{user_id}_{vacancy_id}')
    btn_confirm = InlineKeyboardButton(text='Принять ✅', callback_data=f'confirm_application_{user_id}_{vacancy_id}')
    btn_contact = InlineKeyboardButton(text='Связаться 💬', url=f'tg://user?id={user_id}')

    return InlineKeyboardMarkup(inline_keyboard=[[btn_decline, btn_confirm],
                                                 [btn_contact]])


async def create_inkb_del_applicaion(user_id: int, vacancy_id: int) -> InlineKeyboardMarkup:
    btn_del_application = InlineKeyboardButton(text="Удалить 🗑",
                                               callback_data=f"delete_application_{user_id}_{vacancy_id}")
    return InlineKeyboardMarkup(inline_keyboard=[[btn_del_application]])


async def create_inkb_confirm_del_applicaion(user_id: int, vacancy_id: int) -> InlineKeyboardMarkup:
    btn_back = InlineKeyboardButton(text='Назад ⬅️', callback_data=f'back_delete_application_{user_id}_{vacancy_id}')
    btn_confirm_del_application = InlineKeyboardButton(text="Удалить ✅",
                                                       callback_data=f"confirm_delete_application_{user_id}_{vacancy_id}")
    return InlineKeyboardMarkup(inline_keyboard=[[btn_back, btn_confirm_del_application]])


async def create_inkb_for_sender(btn_text: str, btn_url: str) -> InlineKeyboardMarkup:
    btn_for_sender = InlineKeyboardButton(text=btn_text, url=btn_url)
    return InlineKeyboardMarkup(inline_keyboard=[[btn_for_sender]])
