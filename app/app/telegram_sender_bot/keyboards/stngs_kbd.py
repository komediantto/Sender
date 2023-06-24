from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def stngs_kbd():
    b1 = InlineKeyboardButton(text='Задержка', callback_data='delay')
    b2 = InlineKeyboardButton(text='Текст приветственного сообщения',
                              callback_data='hello_message')
    b3 = InlineKeyboardButton(text='Лимит приветствий',
                              callback_data='hello_limit')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[b1, b3], [b2]],
                                    resize_keyboard=True)
    return keyboard
