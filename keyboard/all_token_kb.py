from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_RU
from database.database import user_db


# функция генерирующая страницу со списком токенов
# в формате {№ токена} - {***Последний 4 символа токена} в виде инлайн кнопок
# и 2-х кнопок "Редактировать" и "Отменить"
def create_all_token_keyboard(user_id: int, *args: str) -> InlineKeyboardMarkup:
    # инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # наполняем клавиатуру кнопками-закладками
    count = 1
    for token in args:
        kb_builder.row(InlineKeyboardButton(
            text=f'№{count}▪{user_db[user_id][token]}▪***{token[-5:]}',
            callback_data=token))
        count += 1
    # Добавляем в клавиатуру в конце две кнопки "Добавить" и "Обновить"
    kb_builder.row(InlineKeyboardButton(text=LEXICON_RU['add'],
                                        callback_data='add'),
                   InlineKeyboardButton(text=LEXICON_RU['update_all'],
                                        callback_data='update_all'),
                   width=2)
    return kb_builder.as_markup()
