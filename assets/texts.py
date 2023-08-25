welcome_text = "приветствие"
employ_or_employer = "Выберите работодатель вы или работник"
employ_warn_info = "as"

start_create = "Заполните форму для создания ваканcии\n для отмены напишите /cancel"
fill_employer = "Напишите организацию"
fill_job = "Напишите должность"
fill_salary = "Напишите зарплату"
fill_minage = "Напишите минимальный возраст"
fill_minexp = "Напишите минимальный опыт работы"
fill_date = "Напишите время или период работы"
fill_short_dsp = "напишите краткое описание вакансии"
fill_long_dsp = "напишите развёрнутое описание вакансии"
confirm_vacancy = "Ваша вакансия:"
cancel_create_vacancy = "Создание вакансии отменено, ваша вакансия удалена"
sure_cancel_create_vacancy = "Вы точно хотите отменить создание вакансии?"
mess12dsh = "Что вы хотите сделать?"



def main_text():
    return "личный кабинет"


def confirm_vacancy_txt(data, type_descr):
    return str(f"*{data.get('employer')}*\n"
               f"{data.get('job')}\n"
               f"{data.get('salary')}\n"
               f"Минимальный возраст \- {data.get('minage')}\n"
               f"Минимальный опыт работы \- {data.get('minexp')}\n"
               f"Время \- {data.get('date')}\n\n"
               f"{data.get('short_dsp' if type_descr == 'short' else 'long_dsp')}")

