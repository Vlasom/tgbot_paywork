from aiogram.fsm.state import StatesGroup, State


class VacancyFormSteps(StatesGroup):
    fill_employer = State()
    fill_job = State()
    fill_salary = State()
    fill_min_age = State()
    fill_min_exp = State()
    fill_date = State()
    fill_short_dsp = State()
    fill_long_dsp = State()
    fill_image = State()
    confirm_create = State()

    edit_employer = State()
    edit_job = State()
    edit_salary = State()
    edit_min_age = State()
    edit_min_exp = State()
    edit_date = State()
    edit_short_dsp = State()
    edit_long_dsp = State()
    edit_image = State()

    create_application = State()


class SenderFormSteps(StatesGroup):
    fill_sender_name = State()
    fill_sender_text = State()
    sender_with_without_image = State()
    fill_sender_image = State()
    sender_with_without_btn = State()
    fill_sender_btn_text = State()
    fill_sender_btn_url = State()

    confirm_sender = State()

