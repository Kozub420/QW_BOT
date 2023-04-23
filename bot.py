import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import handlers, other_handlers
from keyboard.set_menu import set_main_menu

# инициализируем логгер
logger = logging.getLogger(__name__)

# функция конфигурирования и запуска бота
async def main():
    # конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')
    # выводим в консоль инф-ию о старте бота
    logger.info('Starting bot')
    # загружаем конфиг в переменную config
    config: Config = load_config()
    # инициализируем бот и деспетчер
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()
    # настраиваем кнопку Menu
    await set_main_menu(bot)
    # регестрируем роутеры в диспетере
    dp.include_router(handlers.router)
    dp.include_router(other_handlers.router)
    # пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        # запускаем функцию main в ассинхроном режиме
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        logger.error('Bot stopped!!!')
