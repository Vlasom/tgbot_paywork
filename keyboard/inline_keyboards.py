from aiogram.types import InlineKeyboardMarkup
from keyboard.inline_buttons import *

s_vacancy_kb = InlineKeyboardMarkup(inline_keyboard=[[btn_contact, btn_like],
                                                      [btn_more]])

l_vacancy_kb = InlineKeyboardMarkup(inline_keyboard=[[btn_contact, btn_like],
                                                      [btn_less]])


s_create_vac_kb = InlineKeyboardMarkup(inline_keyboard=[[btn_contact, btn_like],
                                                      [btn_less]])


yes_no_kb = InlineKeyboardMarkup(inline_keyboard=[[btn_yes, btn_no]])
