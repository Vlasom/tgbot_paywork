from aiogram.types import InlineKeyboardMarkup
from keyboard.inline_buttons import *

s_vacancy_kb = InlineKeyboardMarkup(inline_keybord=[[btn_contact, btn_like],
                                                      [btn_more]])

l_vacancy_kb = InlineKeyboardMarkup(inline_keybord=[[btn_contact, btn_like],
                                                      [btn_less]])