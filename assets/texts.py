import random

welcome_text = lambda user_id, user_name: \
    f"{random.choice(['Здравствуйте', 'Добрый день', 'Приветствую'])}, <a href='tg://user?id={user_id}'>{user_name}</a>! 👋"

employ_or_employer = ("⬇️ Выберите что хотите сделать\n\n"
                      "• Смотреть самые актуальные вакансии от лица работника 👷‍♂️\n"
                      "  /show_vacancies\n\n"
                      "• Создать вакансию и ждать откликов 📅\n"
                      "  /create_vacancy")

employ_warn_info = ("ℹ️ При просмотре вакансий соблюдайте простые правила\n\n"
                    "• В откликах пишите по делу\n"
                    "• Составляйте грамотные и понятные отклики\n"
                    "• Не используйте нецензурную брань в откликах\n"
                    "• Не спамьте\n\n"
                    "❗️ Пожалуйста, уважайте себя и других пользователей бота")

no_vacancies_notification = ("Больше вакансий нет 🤷‍♂️\n\n"
                             "На данный момент вы просмотрели все актуальные вакансии\n\n"
                             "Но мы можем уведомить вас, когда появится новая вакансия 🆕")

no_vacancies_msg = ("Больше вакансий нет 🤷‍♂️\n\n"
                    "На данный момент вы просмотрели все актуальные вакансии\n\n"
                    "Но вы можете посмотреть эти же вакансии еще раз 🔂")

ok_bro_msg = ("Я все понял! 👌\n\n"
              "Буду с нетерпеньем ждать вас, мой дорогой друг! 🤝\n\n"
              "• Когда вернётесь, просто нажмите на кнопку снизу ⬇️\n\n"
              "• Или напишите команду\n"
              "  /main_page")

creating_vacancy_application = ("📩 Напишите свой отклик в одном сообщении\n\n"
                                "• Если вы передумали, нажмите на кнопку снизу ⬇️\n\n"
                                "• Или введите команду\n"
                                "  /cancel")

new_vacancy_msg = "🆕 Появилась новая вакансия!"

already_save_application = ("🔔 На эту вакансию вы уже откликнулись\n\n"
                            "Пожалуйста ожидайте ответа работодателя")

save_application = "✅ Ваш отклик успешно сохранен"
cancel_create_application = "❌ Создание отклика отменено"

like_notification = "✅ Вакансия добавлена в изранные"
nlike_notification = "❌ Вакансия удалена из изранных"

# добавить снизу кнопку команды - "посмотреть commands", чтобы посмотреть список всех команд и их действия
help_txt = ("💰 PayWork – Подработка \n\n"
            "🤖 Я бот, созданный для помощи несовершеннолетним и студентам с поиском подработки."
            "Любой желающий может оперативно найти себе работу на лето или каникулы\n\n"

            "• Вы можете искать и откликаться на актуальные вакансии в городе Мирный\n"
            "  /show_vacancies\n\n"

            "• Также работодатели могут создавать свои вакансии для поиска работников\n"
            "  /create_vacancy\n\n"

            "📃 Также вы можете ознакомиться с полным списком команд и их описаниями\n"
            "  /commands\n\n"

            "🆘 Если возникут трудности или появятся вопроcы по работе бота - свяжитесь с разработчиками\n\n"
            "  @TraffMinister\n"
            "  @vlasom")



# no_favorite_vacancies
no_favorites = ("📂 Вы не добавили ни одну вакансию в избранные\n\n"
                "• Чтобы добавить их прямо сейчас, нажмите на кнопку снизу ⬇️\n\n"
                "• Или введите команду\n"
                "  /show_vacancies")

# no_created_vacancies
no_created = ("📭 Вы еще не создали ни одной вакансии\n\n"
              "• Чтобы создать вакансию, нажмите на кнопку снизу ⬇️\n\n"
              "• Или введите команду\n"
              "  /create_vacancy")

# Где используется???
no_application = "На эту вакансию ещё нет откликов"

unverified_user = ("Чтобы создать вакансии необходимо подтвердить личность.\n "
                   "Пожалуйста, напишите @TraffMinister или @vlasom ")

# create_vacancy
start_create = ("✏️ Заполните форму для создания ваканcии\n\n"
                "• Для отмены нажмите на кнопку внизу ⬇️\n\n"
                "• Или напишите команду\n"
                "  /cancel")

employ_verification = "Вы должнеы и тд и тп"

fill_employer = "🔰 Введите наименование организации или физическое лицо, предоставляющее работу"
fill_job = "🔰 Введите требуемую должность или работу для выполнения"
fill_salary = "🔰 Введите предлагаемую заработную плату"
fill_min_age = "🔰 Введите требуемый минимальный возраст работника"
fill_min_exp = "🔰 Введите требуемый минимальный опыт работы"
fill_date = "🔰 Введите период работы"
fill_short_dsp = "🔰 Введите краткое описание вакансии"
fill_long_dsp = "🔰 Введите развёрнутое описание вакансии"

fill_image = ("🔰 Превью вашей вакансии по умолчанию\n\n"
              "• По желанию, можно её изменить, отправив новое изображение\n\n"
              "• Или вы можете оставить эту картинку 🌄")
edit_standard_image = "🔰 Превью вашей вакансии по умолчанию\n\n"

fill_new_image = "🔰 Отправьте изображение или выберите по умолчанию"
confirm_vacancy = "⬇️ Ваша вакансия ⬇️"

sure_cancel_create_vacancy = "❓ Вы точно хотите отменить создание вакансии и удалить форму?"
cancel_create_vacancy = "❌ Создание вакансии отменено, ваша форма удалена"

callback_in_creating_vacancy = "❗️ Для начала завершите или отмените создание вакансии"
callback_in_creating_application = "❗️ Для начала завершите или отмените создание заявки"
callback_in_default_state = "❗️ Сейчас данная кнопка не длступна"

command_in_creating_vacancy = "⛔️ Вы не можете воспользоваться этой командой во время создания вакансии"
command_in_creating_application = "⛔️ Вы не можете воспользоваться этой командой во время создания заявки"

command_doesnt_exist = ("⛔️ Такой команды не существует\n\n"
                        "Вот список доступных команд ⬇️")  # Здесь можно отправлять спмок доступных команд

command_cancel_in_default_state = ("Вам нечего отменять.\n"
                                   "Если меню с коммандами не обновилось, "
                                   "попробуйте написать /start и перезайти в чат с ботом")

random_msg = ("Я не совсем вас понял 🤷‍♂️\n\n"
              "Вот что вы можете сделать ⬇️")

warning_spam_msg = "❗️ Убедительная просьба не спамить!"
waning_u_are_stupid = "💥 Ой, что-то пошло не так..."

my_editing_vacancy = "⬇️ Редактируемая вакансия ⬇️"
undo_editing = "❌ Редактиование вакансии отменено"
delete_vacancy = "❌ Удалена вакансия №"

edit_employer = "⬇️ Ваша вакансия ⬇️"
edit_job = "⬇️ Ваша вакансия ⬇️"
edit_salary = "⬇️ Ваша вакансия ⬇️"
edit_minage = "⬇️ Ваша вакансия ⬇️"
edit_minexp = "⬇️ Ваша вакансия ⬇️"
edit_date = "⬇️ Ваша вакансия ⬇️"
edit_short_dsp = "⬇️ Ваша вакансия ⬇️"
edit_long_dsp = "⬇️ Ваша вакансия ⬇️"
edit_image = "⬇️ Ваша вакансия ⬇️"


what_you_can = "Вот что вы можете сделать 👇"
main_page = "Вот что вы можете сделать 👇"

awaitable_image = "❗️ Пожалуйста, отправьте изображение"
no_vacancy_application = "❗️ На эту вакансию у вас ещё нет заявок"

no_user_application = ("❗️ У вас пока что нет откликов\n\n"
                       "• Но вы можете посмотреть вакансии и оставить свой отклик ⬇️"
                       "  /view_vacancies")




warning_msg = "ТЫ ШО, ТУПОЙ ЧТОЛЕ о_О?\nЧИТАТЬ НЕ УМЕЕШЬ?\nИДИ ОБРАТНО В ШКОЛУ, УПЫРЬ"