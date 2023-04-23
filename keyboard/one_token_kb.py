from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_RU


# функция генерирующая страницу с информацией о токене
# кнопок "история" и "Обновить"
# и кнопки "Список Токенов"
def create_one_token_keyboard() -> InlineKeyboardMarkup:
    # инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Добавляем в клавиатуру в конце две кнопки "История" и "Обновить"
    kb_builder.row(InlineKeyboardButton(text=LEXICON_RU['history'],
                                        callback_data='history'),
                   InlineKeyboardButton(text=LEXICON_RU['update_one'],
                                        callback_data='update_one'),
                   width=2)
    # наполняем клавиатуру кнопкой "Список токенов"
    kb_builder.row(InlineKeyboardButton(
                        text=LEXICON_RU['start_kb'],
                        callback_data='start_kb')
                )
    return kb_builder.as_markup()
