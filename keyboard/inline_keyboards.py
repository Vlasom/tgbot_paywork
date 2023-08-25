from aiogram.types import InlineKeyboardMarkup
from keyboard.inline_buttons import *

s_vacancy_kb = InlineKeyboardMarkup(inline_keyboard=[[btn_contact, btn_like],
                                                      [btn_more]])

l_vacancy_kb = InlineKeyboardMarkup(inline_keyboard=[[btn_contact, btn_like],
                                                      [btn_less]])


s_create_vac_kb = InlineKeyboardMarkup(inline_keyboard=[[btn_contact, btn_like],
                                                      [btn_less]])


yes_no_kb = InlineKeyboardMarkup(inline_keyboard=[[btn_yes, btn_no]])


edit_vac_kb = InlineKeyboardMarkup(inline_keyboard=[[btn_edit_employer],
                                            [btn_edit_job],
                                            [btn_edit_salary],
                                            [btn_edit_minage],
                                            [btn_edit_minexp],
                                            [btn_edit_date],
                                            [btn_edit_short_dsp],
                                            [btn_edit_long_dsp]])