from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from database.database import user_db


class IsTokenCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data in user_db[callback.from_user.id]


"""
class IsDelBookmarkCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return isinstance(callback.data, str) and 'del' in callback.data and callback.data[:-3].isdigit()
"""