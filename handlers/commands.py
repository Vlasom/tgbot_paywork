from tgbot import *


async def start_command(message: types.Message):
    await message.reply(texts.welcome_text)
    await asyncio.sleep(0.5)

    markup = InlineKeyboardMarkup(inline_keyboard=[[
        inline_buttons.btn_employer,
        inline_buttons.btn_employ]])

    await message.reply(text=texts.employ_or_employer, reply_markup=markup)


async def choice_command(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        inline_buttons.btn_employer,
        inline_buttons.btn_employ]])

    await message.reply(text=texts.employ_or_employer, reply_markup=markup)
