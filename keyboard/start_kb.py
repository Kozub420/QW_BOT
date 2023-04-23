from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_RU


# функция генерирующая кнопку старт
# используется в при команде '/start'
# и переходе к списку с токенами
def create_start_keyboard() -> InlineKeyboardMarkup:
    # инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # наполняем клавиатуру кнопкой "Список токенов"
    kb_builder.row(InlineKeyboardButton(
        text=LEXICON_RU['start_kb'],
        callback_data='start_kb')
    )
    return kb_builder.as_markup()
