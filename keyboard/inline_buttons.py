from aiogram.types import InlineKeyboardButton

btn_employer = InlineKeyboardButton(text='Создать заявку', callback_data='employer')
btn_employ = InlineKeyboardButton(text='Смотреть вакансии', callback_data='employ')

btn_next = InlineKeyboardButton(text='Следующаю', callback_data='next')
btn_more = InlineKeyboardButton(text='Подробнее', callback_data='more')
btn_like = InlineKeyboardButton(text='В избранное', callback_data='like')
btn_less = InlineKeyboardButton(text='Свернуть', callback_data='like')

