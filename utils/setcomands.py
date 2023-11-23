from aiogram.types import BotCommand, BotCommandScopeChat
from aiogram import Bot
from classes import redis_commands
from classes.Users import User


# на бета тесте проверить у всех ли будут меняться команды без перезахода
async def set_default_commands(bot: Bot, chat_id: int, user: User) -> None:
    commands_list = [BotCommand(command="/start", description="Перезапуск бота"),
                     BotCommand(command="/help", description="Помощь"),
                     BotCommand(command="/view_vacancies", description="Просмотр вакансий"),
                     BotCommand(command="/favorites", description="Избранные"),
                     BotCommand(command="/my_applications", description="Мои отклики")]
    if await redis_commands.check_verification(user):
        commands_list.extend([BotCommand(command="/create_vacancy", description="Создание вакансии"),
                              BotCommand(command="/my_vacancies", description="Мои вакансии")])

    await bot.set_my_commands(commands=commands_list, scope=BotCommandScopeChat(chat_id=chat_id))


async def set_cancel_create_vacancy_command(bot: Bot, chat_id: int) -> None:
    commands_list = [BotCommand(command="/cancel", description="Отмена создания вакансии")]
    await bot.set_my_commands(commands=commands_list, scope=BotCommandScopeChat(chat_id=chat_id))


async def set_cancel_edit_command(bot: Bot, chat_id: int) -> None:
    commands_list = [BotCommand(command="/cancel", description="Отмена редактирования")]
    await bot.set_my_commands(commands=commands_list, scope=BotCommandScopeChat(chat_id=chat_id))


async def set_cancel_create_application_command(bot: Bot, chat_id: int) -> None:
    commands_list = [BotCommand(command="/cancel", description="Отмена создания заявки")]
    await bot.set_my_commands(commands=commands_list, scope=BotCommandScopeChat(chat_id=chat_id))
