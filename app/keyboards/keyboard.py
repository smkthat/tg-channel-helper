from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.handlers.callbacks.callback import AdminCallback

BOT_URL_FORMAT = 'https://t.me/{bot_username}?start='


# def get_start_keyboard() -> InlineKeyboardMarkup:
#     return InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text='Телеграм',
#                                   url='https://t.me/utromagadana')],
#             [InlineKeyboardButton(text='Одноклассники',
#                                   url='https://ok.ru/utromagadana')],
#             [InlineKeyboardButton(text='ВКонтакте',
#                                   url='https://vk.com/utromagadana')]
#         ]
#     )


def get_admin_start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text='Управление каналом',
                callback_data=AdminCallback(action=AdminCallback.Action.CHANNEL,
                                            data='menu').pack()
            )],
            [InlineKeyboardButton(
                text='Рассылка',
                callback_data=AdminCallback(
                    action=AdminCallback.Action.NEWSLETTER, data='menu').pack()
            )]
        ]
    )


def get_channel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text='Создать сообщение',
                callback_data=AdminCallback(
                    action=AdminCallback.Action.CREATE_MESSAGE,
                    data='menu').pack()
            )],
        ])


def get_bot_link_keyboard(bot_username: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text='Прислать новость',
                url=BOT_URL_FORMAT.format(bot_username)
            )
        ]]
    )


def get_accept_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text='✅Да',
                callback_data=AdminCallback(
                    action=AdminCallback.Action.ACCEPT,
                    data='yes'
                ).pack()
            ),
            InlineKeyboardButton(
                text='❌Нет',
                callback_data=AdminCallback(
                    action=AdminCallback.Action.ACCEPT,
                    data='no'
                ).pack()
            )
        ]]
    )


def get_keyboard_from_data(
        buttons_data: list[list[dict]]
) -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(**button) for button in row]
        for row in buttons_data
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
