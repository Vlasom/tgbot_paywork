from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from classes import *
from assets.texts import notification_buttons


class NotifiCallbackFactory(CallbackData, prefix='notification'):
    place: int
    # 1 - телеграм, 2 - почта
    event: int
    # 1 - новая вакансия, 2 - удалено из избранных, 3 - ответили на отклик
    status: int





async def create_inkb_user_notifications(user: User):
    inkb_notification_builder = InlineKeyboardBuilder()
    user_notification = await vac_notification.get_user_notifications(user)
    print(user_notification)

    inkb_notification_builder.button(
        text="Новая вакансия", callback_data="new_vacancy_notifications")

    inkb_notification_builder.button(
        text=notification_buttons["tg"][user_notification["tg"][1]],
        callback_data=NotifiCallbackFactory(
            place=1,
            event=1,
            status=user_notification["tg"][1]
        )
    )

    inkb_notification_builder.button(
        text=notification_buttons["email"][user_notification["email"][1]],
        callback_data=NotifiCallbackFactory(
            place=2,
            event=1,
            status=user_notification["email"][1]
        )
    )

    inkb_notification_builder.button(
        text="Удалено из избранных", callback_data="del_from_likes_notifications")

    inkb_notification_builder.button(
        text=notification_buttons["tg"][user_notification["tg"][2]],
        callback_data=NotifiCallbackFactory(
            place=1,
            event=2,
            status=user_notification["tg"][2]
        )
    )
    inkb_notification_builder.button(
        text=notification_buttons["email"][user_notification["email"][2]],
        callback_data=NotifiCallbackFactory(
            place=2,
            event=2,
            status=user_notification["email"][2]
        )
    )

    inkb_notification_builder.button(
        text="Ответ на отклик", callback_data="application_answer_notifications")

    inkb_notification_builder.button(
        text=notification_buttons["tg"][user_notification["tg"][3]],
        callback_data=NotifiCallbackFactory(
            place=1,
            event=3,
            status=user_notification["tg"][3]
        )
    )
    inkb_notification_builder.button(
        text=notification_buttons["email"][user_notification["email"][3]],
        callback_data=NotifiCallbackFactory(
            place=2,
            event=3,
            status=user_notification["email"][3]
        )
    )

    return inkb_notification_builder.adjust(1, 2, repeat=True).as_markup()

