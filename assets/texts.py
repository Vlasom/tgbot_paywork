welcome_text = "приветствие"
employ_or_employer = "Выберите работодатель вы или работник"
employ_warn_info = "as"

start_create = "Заполните форму для создания ваканcии\n для отмены напишите /cancel"
fill_employer = "Напишите организацию"
fill_job = "Напишите необходимую должность"
fill_salary = "Напишите предлагаемую зарплату"
fill_minage = "Напишите требуемого минимального возраста"
fill_minexp = "Напишите требуемый минимальный опыт работы"
fill_date = "Напишите время или период работы"
fill_short_dsp = "Напишите краткое описание вакансии"
fill_long_dsp = "Напишите развёрнутое описание вакансии"
confirm_vacancy = "Ваша вакансия:"
cancel_create_vacancy = "Создание вакансии отменено, ваша вакансия удалена"
sure_cancel_create_vacancy = "Вы точно хотите отменить создание вакансии?"
mess12dsh = "Что вы хотите сделать?"


warning_msg = "Такой тип данных не обрабатывается, напишите текстом, пожалуйста"

edit_employer = "обновлена организацию"
edit_job = "обновлена должность"
edit_salary = "обновлена зарплату"
edit_minage = "обновлена минимальный возраст"
edit_minexp = "обновлена минимальный опыт работы"
edit_date = "обновлена время или период работы"
edit_short_dsp = "обновлена краткое описание вакансии"
edit_long_dsp = "обновлена развёрнутое описание вакансии"




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

