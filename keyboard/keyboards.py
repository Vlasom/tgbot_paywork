from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from keyboard.keyboards_buttons import *

confirm_create_kb = ReplyKeyboardMarkup(keyboard=[[btn_edit],
                                                  [btn_cancel, btn_save]], resize_keyboard=True)