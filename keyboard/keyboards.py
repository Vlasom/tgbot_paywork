from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import KeyboardButton

btn_cancel = KeyboardButton(text='Отменить')
btn_save = KeyboardButton(text='Сохранить')
btn_edit = KeyboardButton(text='Редактировать')


kb_confirm_create = ReplyKeyboardMarkup(keyboard=[[btn_edit],
                                                  [btn_cancel, btn_save]], resize_keyboard=True)