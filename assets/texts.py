welcome_text = "приветствие"
employ_or_employer = "Выберите работодатель вы или работник"
employ_warn_info = "as"

start_create = "Заполните форму для создания ваканcии\n для отмены напишите /cancel"
fill_employer = "Напишите организацию"
fill_job = "Напишите необходимую должность или работу для выполнения"
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


edit_employer = "обновлена организацию\nВаша вакансия:"
edit_job = "обновлена должность\nВаша вакансия:"
edit_salary = "обновлена зарплату\nВаша вакансия:"
edit_minage = "обновлена минимальный возраст\nВаша вакансия:"
edit_minexp = "обновлена минимальный опыт работы\nВаша вакансия:"
edit_date = "обновлена время или период работы\nВаша вакансия:"
edit_short_dsp = "обновлена краткое описание вакансии\nВаша вакансия:"
edit_long_dsp = "обновлена развёрнутое описание вакансии\nВаша вакансия:"

warning_msg = "ТЫ ШО, ТУПОЙ ЧТОЛЕ о_О?\nЧИТАТЬ НЕ УМЕЕШЬ?\nИДИ ОБРАТНО В ШКОЛУ, УПЫРЬ"





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

