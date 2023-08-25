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


