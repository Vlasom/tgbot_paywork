from aiogram.fsm.state import StatesGroup, State

class StapesForm(StatesGroup):
    fill_employer = State()
    fill_job = State()
    fill_salary = State()
    fill_minage = State()
    fill_minexp = State()
    fill_date = State()
    fill_short_dsp = State()
    fill_long_dsp = State()
    confirm_create = State()

    edit_values = State()

    edit_employer = State()
    edit_job = State()
    edit_salary = State()
    edit_minage = State()
    edit_minexp = State()
    edit_date = State()
    edit_short_dsp = State()
    edit_long_dsp = State()




