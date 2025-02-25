from aiogram.types import BotCommand


# Функция для настройки кнопки Menu бота
async def set_main_menu(bot):
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/help',
                   description='Взаимодействие с ботом'),
        BotCommand(command='/send',
                   description='Отправить сообщение через бота')
        ]
    await bot.set_my_commands(main_menu_commands)

