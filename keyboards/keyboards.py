from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

_btn_cancel = KeyboardButton(text='Отменить ❌')
_btn_save = KeyboardButton(text='Сохранить ✅')
_btn_edit = KeyboardButton(text='Редактировать ✏️')


kb_confirm_create = ReplyKeyboardMarkup(keyboard=[[_btn_edit],
                                                  [_btn_cancel, _btn_save]], resize_keyboard=True)