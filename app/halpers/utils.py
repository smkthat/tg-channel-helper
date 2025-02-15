from contextlib import suppress

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext


def chunks(target: list, count: int):
    """This function takes a list and an integer as input and yields a generator object.

    The generator yields sub-lists of the input list with a maximum length equal to the input integer value.
    The purpose of this function is to split a large list into smaller sub-lists,
    each with a maximum number of elements equal to count.
    """
    for i in range(0, len(target), count):
        yield target[i:i + count]


async def add_ui_messages(messages_ids: list[int], state: FSMContext) -> None:
    if data := await state.get_data():
        ui_messages = data.get('ui_messages', [])
        ui_messages.extend(messages_ids)
        await state.update_data(ui_messages=ui_messages)


async def delete_ui_messages(bot: Bot, state: FSMContext) -> None:
    if data := await state.get_data():
        ui_messages = data.get('ui_messages', [])
        for message_id in reversed(ui_messages):
            await delete_or_edit_message(chat_id=state.key.chat_id, message_id=message_id, bot=bot)


async def delete_or_edit_message(chat_id: int, message_id: int, bot: Bot):
    with suppress(TelegramBadRequest):
        if not await bot.delete_message(chat_id=chat_id, message_id=message_id):
            await bot.edit_message_text(
                text='᠌ ᠌ ᠌᠌ ᠌ ᠌ ᠌ ᠌ ᠌',
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=None
            )
