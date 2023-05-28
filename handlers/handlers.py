from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery
from services.services import balance, get_restrictions, history_list, info_profile
from lexicon.lexicon import LEXICON_RU

from keyboard.all_token_kb import create_all_token_keyboard
from keyboard.start_kb import create_start_keyboard
from keyboard.one_token_kb import create_one_token_keyboard

from database.database import user_db
from filters.filters import IsTokenCallbackData

router: Router = Router()


# Хендлер на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'],
                         reply_markup=create_start_keyboard()
                         )


# Хендлер на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Этот хэндлер будет срабатывать на команду "/all"
# и отправлять пользователю список сохраненных закладок,
# если они есть или сообщение о том, что закладок нет
@router.message(Command(commands='all'))
async def process_all_command(message: Message):
    if message.from_user.id in user_db:
        await message.answer(text=LEXICON_RU[message.text],
                             reply_markup=create_all_token_keyboard(message.from_user.id,
                                                                    *user_db[message.from_user.id])
                             )
    else:
        await message.answer(text=LEXICON_RU["no_db"])


# Хендлер на команду /history + токен
@router.message(Command(commands='history'), lambda message: len(message.text[9:]) == 32)
async def process_history_command(message: Message):
    await message.answer(text=history_list(message.text[9:]))


# Сокращенная команда /history
# Хендлер на команду /h + токен
@router.message(Command(commands='h'), lambda message: len(message.text[3:]) == 32)
async def process_h_command(message: Message):
    await message.answer(text=history_list(message.text[3:]))


# Хендлер на команду /token + токен
@router.message(Command(commands='token'), lambda message: len(message.text[7:]) == 32)
async def process_token_command(message: Message):
    balances = balance(message.text[7:])['accounts']
    await message.answer(text=f"Баланс: {balances[0]['balance']['amount']} RUB\n")


# сокращенная команда /token
# Хендлер на команду /t+токен
@router.message(Command(commands='t'), lambda message: len(message.text[3:]) == 32)
async def process_t_command(message: Message):
    balances = balance(message.text[3:])['accounts']
    await message.answer(text=f"Баланс: {balances[0]['balance']['amount']} RUB\n")


# Хендлер на команду /block + токен
@router.message(Command(commands='block'), lambda message: len(message.text[7:]) == 32)
async def process_block_command(message: Message):
    check_in_block = get_restrictions(message.text[7:])
    if not check_in_block:
        await message.answer(text="На кошельке нет блокировок! ✅\n")
    else:
        await message.answer(text=f"{check_in_block}\n")


# сокращенная команда /block
# Хендлер на команду /b + токен
@router.message(Command(commands='b'), lambda message: len(message.text[3:]) == 32)
async def process_block_command(message: Message):
    check_in_block = get_restrictions(message.text[3:])
    if not check_in_block:
        await message.answer(text="На кошельке нет блокировок! ✅\n")
    else:
        await message.answer(text=f"{check_in_block}\n")


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Список токенов!"
@router.callback_query(Text(text='start_kb'))
async def process_start_kb_press(callback: CallbackQuery):
    if callback.from_user.id in user_db:
        await callback.message.edit_text(
                                text=LEXICON_RU['/all'],
                                reply_markup=create_all_token_keyboard(callback.from_user.id,
                                                                       *user_db[callback.from_user.id])
                                )
    else:
        await callback.message.edit_text(text=LEXICON_RU["no_db"])
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки из списка токенов
@router.callback_query(IsTokenCallbackData())
async def process_token_press(callback: CallbackQuery):
    #current_token = callback.data
    await callback.message.edit_text(
                                # callback.data = это токен выбранного кошелька
                                text=info_profile(callback.from_user.id, callback.data),
                                reply_markup=create_one_token_keyboard(),
                                parse_mode='HTML'
                                )
    await callback.answer('Токен выбран!')


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "История"
@router.callback_query(Text(text='history'))
async def process_history_press(callback: CallbackQuery):
    await callback.message.edit_text(
                                text='history_list(current_token)',
                                reply_markup=create_start_keyboard()
                                )
    await callback.answer()
