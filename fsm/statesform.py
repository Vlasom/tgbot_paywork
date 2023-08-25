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



