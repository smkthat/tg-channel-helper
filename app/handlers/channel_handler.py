from typing import List

from aiogram import Dispatcher, Bot, F
from aiogram.enums import ContentType, ChatType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ForceReply
from aiogram_media_group import media_group_handler

from app.configuration.config_loader import CONFIG
from app.configuration.log import get_logger
from app.halpers.utils import add_ui_messages, delete_ui_messages, \
    delete_or_edit_message
from app.handlers.callbacks.callback import AdminCallback
from app.handlers.filters.filter import AdminChatFilter
from app.handlers.menu_handler import delete_menu, start_admin_call
from app.handlers.states.state import ChannelSG
from app.keyboards.keyboard import get_bot_link_keyboard, get_accept_keyboard

LOGGER = get_logger(__name__, '../../logs')


async def create_message(c: CallbackQuery, bot: Bot, state: FSMContext):
    await delete_menu(c.message, bot, state)
    await state.set_state(ChannelSG.create_message)
    await c.answer(
        text=(
            '! В сообщении может быть не больше одного медиа файла'
            '\n\nК сообщению будет прикреплена кнопка "Прислать новость" '
            'с ссылкой на чат с ботом'
        ),
        show_alert=True
    )
    ui_message = await c.message.answer(
        text='➕Пришлите ваше сообщение',
        reply_markup=ForceReply()
    )
    await add_ui_messages([ui_message.message_id], state)
    await c.answer()


@media_group_handler
async def input_created_message_album(
        messages: List[Message],
        bot: Bot,
        state: FSMContext
):
    m = messages.pop(0)
    for message in messages:
        await delete_or_edit_message(
            chat_id=message.chat.id,
            message_id=message.message_id,
            bot=bot
        )

    return await input_created_message(m, bot, state)


async def input_created_message(m: Message, bot: Bot, state: FSMContext):
    bot_user = await bot.get_me()
    new_message = await m.copy_to(
        chat_id=m.chat.id,
        reply_markup=get_bot_link_keyboard(bot_user.username)
    )
    await bot.pin_chat_message(
        chat_id=m.chat.id,
        message_id=new_message.message_id,
        disable_notification=True
    )
    await delete_or_edit_message(
        chat_id=m.chat.id,
        message_id=m.message_id,
        bot=bot
    )
    await state.set_state(ChannelSG.accept_create_message)
    await state.update_data(tmp_message_id=new_message.message_id)
    await add_ui_messages(messages_ids=[new_message.message_id], state=state)
    accept_m = await m.answer(
        text='Подтвердить отправку?',
        reply_markup=get_accept_keyboard()
    )
    await add_ui_messages(messages_ids=[accept_m.message_id], state=state)


async def accept_create_message(
        c: CallbackQuery,
        callback_data: AdminCallback,
        bot: Bot,
        state: FSMContext
):
    if data := await state.get_data():
        match callback_data.data:
            case 'yes':
                if channel_id := CONFIG.bots[bot.id].channel_id:
                    bot_user = await bot.get_me()
                    await bot.copy_message(
                        chat_id=channel_id,
                        from_chat_id=c.message.chat.id,
                        message_id=data['tmp_message_id'],
                        reply_markup=get_bot_link_keyboard(bot_user.url)
                    )
                    await c.answer(
                        text='Сообщение отправлено на канал', show_alert=True
                    )
                else:
                    await c.answer(
                        text='❌ Не удалось определить канал', show_alert=True
                    )
            case 'no':
                await c.answer(text='❌ Вы отменили отправку сообщения')

    await delete_or_edit_message(
        chat_id=c.message.chat.id,
        message_id=data['tmp_message_id'],
        bot=bot
    )
    await delete_or_edit_message(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        bot=bot
    )
    await delete_ui_messages(bot=bot, state=state)
    await state.clear()
    await start_admin_call(c, bot, state)


def register_channel_handlers(dp: Dispatcher):
    dp.callback_query.register(
        create_message,
        AdminCallback.filter(F.action == AdminCallback.Action.CREATE_MESSAGE),
        AdminChatFilter(),
        lambda call: call.message.chat.type == ChatType.PRIVATE
    )
    dp.message.register(
        input_created_message_album,
        F.media_group_id,
        AdminChatFilter(),
        lambda message: message.chat.type == ChatType.PRIVATE,
        lambda message: message.content_type in [
            ContentType.PHOTO,
            ContentType.VIDEO,
            ContentType.DOCUMENT
        ],
        ChannelSG.create_message
    )
    dp.message.register(
        input_created_message,
        AdminChatFilter(),
        lambda message: message.chat.type == ChatType.PRIVATE,
        ChannelSG.create_message
    )
    dp.callback_query.register(
        accept_create_message,
        AdminCallback.filter(F.action == AdminCallback.Action.ACCEPT),
        AdminChatFilter(),
        lambda call: call.message.chat.type == ChatType.PRIVATE,
        ChannelSG.accept_create_message
    )
