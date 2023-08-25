from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

btn_employer = InlineKeyboardButton(text='Создать заявку', callback_data='employer')
btn_employ = InlineKeyboardButton(text='Смотреть вакансии', callback_data='employ')

btn_contact = InlineKeyboardButton(text='Связаться', callback_data='contact')
btn_next = InlineKeyboardButton(text='Следующаю', callback_data='next')
btn_more = InlineKeyboardButton(text='Подробнее', callback_data='more')
btn_like = InlineKeyboardButton(text='В избранное', callback_data='like')
btn_less = InlineKeyboardButton(text='Свернуть', callback_data='less')

btn_yes = InlineKeyboardButton(text='Да', callback_data='canceling')
btn_no = InlineKeyboardButton(text='Нет', callback_data='continue')

btn_edit_employer = InlineKeyboardButton(text='Организация', callback_data='edit_employer')
btn_edit_job = InlineKeyboardButton(text='Должность', callback_data='edit_job')
btn_edit_salary = InlineKeyboardButton(text='Зарплата', callback_data='edit_salary')
btn_edit_minage = InlineKeyboardButton(text='Минимальный возраст', callback_data='edit_minage')
btn_edit_minexp = InlineKeyboardButton(text='Минимальный опыт работы', callback_data='edit_minexp')
btn_edit_date = InlineKeyboardButton(text='Время', callback_data='edit_date')
btn_edit_short_dsp = InlineKeyboardButton(text='Краткое описание', callback_data='edit_short_dsp')
btn_edit_long_dsp = InlineKeyboardButton(text='Подробное описание', callback_data='edit_long_dsp')

btn_cancel = InlineKeyboardButton(text='Отменить', callback_data='vacancy_cancel')
btn_save = InlineKeyboardButton(text='Сохранить', callback_data='vacancy_save')
btn_edit = InlineKeyboardButton(text='Редактировать', callback_data='vacancy_edit')
btn_back = InlineKeyboardButton(text='Назад', callback_data='back')


inkb_employ_employer = InlineKeyboardMarkup(inline_keyboard=[[
        btn_employer,
        btn_employ]])

inkb_contact_like_more_next = InlineKeyboardMarkup(inline_keyboard=[[
        btn_contact, btn_more,
        btn_like],
        [btn_next]])

inkb_contact_like_more = InlineKeyboardMarkup(inline_keyboard=[[
    btn_contact, btn_like],
            [btn_more]])

inkb_contact_like_less_next = InlineKeyboardMarkup(inline_keyboard=[[
            btn_contact, btn_less,
            btn_like],
            [btn_next]])

inkb_contact_like_less = InlineKeyboardMarkup(inline_keyboard=[[btn_contact, btn_like],
                                                      [btn_less]])


inkb_yes_no = InlineKeyboardMarkup(inline_keyboard=[[btn_yes, btn_back]])


inkb_edit_vac = InlineKeyboardMarkup(inline_keyboard=[[btn_edit_employer],
                                            [btn_edit_job],
                                            [btn_edit_salary],
                                            [btn_edit_minage],
                                            [btn_edit_minexp],
                                            [btn_edit_date],
                                            [btn_edit_short_dsp],
                                            [btn_edit_long_dsp],
                                            [btn_back]])

inkb_edit_cancel_save = InlineKeyboardMarkup(inline_keyboard=[[btn_edit],
                                        [btn_cancel, btn_save]])