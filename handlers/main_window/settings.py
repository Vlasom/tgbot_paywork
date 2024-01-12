from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.state import default_state
from assets import texts
from aiogram import Router, F
from aiogram.filters import StateFilter

from classes import vac_commands, User, Vacancy, db_commands, redis_commands
from keyboards.inline_keyboards import *

router = Router()
router.callback_query.filter(StateFilter(default_state))


@router.callback_query(F.data == "settings_notification")
async def settings_notification(callback: CallbackQuery):
    pass
