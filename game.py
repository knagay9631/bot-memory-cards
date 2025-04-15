import asyncio
import logging
import random


from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram import F
import button_1


TOKEN = "7815225009:AAGr4B1GfdYU6dAlzBhwq2dGe6N174D6pZA"
dp = Dispatcher(storage=MemoryStorage())
cards = []
closed_cards = [
    ["00", "01", "02", "03"],
    ["10", "11", "12", "13"],
    ["20", "21", "22", "23"],
    ["30", "31", "32", "33"],
]
user_cards_coord = []


@dp.message(CommandStart())
async def command_start_handler(message:Message) -> None:
    global closed_cards, cards
    closed_cards = [
        ["00", "01", "02", "03"],
        ["10", "11", "12", "13"],
        ["20", "21", "22", "23"],
        ["30", "31", "32", "33"],
    ]
    line_1 = ["😊", "😫", "💋", "🦹🏼‍♂"]
    random.shuffle(line_1)
    line_2 = ["😎", "😇", "🥳", "🤣"]
    random.shuffle(line_2)
    line_3 = ["😊", "😫", "💋", "🦹🏼‍♂"]
    random.shuffle(line_3)
    line_4 = ["😎", "😇", "🥳", "🤣"]
    random.shuffle(line_4)
    
    cards = [ line_1, line_2, line_3, line_4 ]
    random.shuffle(cards)

    buttons = button_1.create_button(closed_cards)
    await message.answer(f"Hello {message.from_user.full_name} :)", reply_markup=buttons)


@dp.message()
async def echo_handler(message: Message) -> None:
    global closed_cards, cards, user_cards_coord

    if closed_cards == cards:
        return

    isCardFounded = False
    for line in closed_cards:
        if message.text in line:
            isCardFounded = True
    
    if not isCardFounded:
        await message.answer(f"Пожалуйста нажмите на одну из карточек")
        return
    
    coord = message.text
    if not coord.isdigit():
        return
    
    if len(user_cards_coord) > 1:
        if closed_cards[user_cards_coord[0][0]][user_cards_coord[0][1]] == closed_cards[user_cards_coord[1][0]][user_cards_coord[1][1]]:
            user_cards_coord = []
            await message.answer(f"Угадал!!! Ищи теперь остальные")
            
        # закрытие карточек на клавиатуре пользователя
        else:
            closed_cards[user_cards_coord[0][0]][user_cards_coord[0][1]] = str(user_cards_coord[0][0]) + str(user_cards_coord[0][1])
            closed_cards[user_cards_coord[1][0]][user_cards_coord[1][1]] = str(user_cards_coord[1][0]) + str(user_cards_coord[1][1])
            user_cards_coord = []
    
    
    first_card_x = int(coord[0])
    first_card_y = int(coord[1])
    user_cards_coord.append([first_card_x, first_card_y])
    closed_cards[first_card_x][first_card_y] = cards[first_card_x][first_card_y]
    
    buttons = button_1.create_button(closed_cards)
    
    await message.answer(f"Карточка открыта", reply_markup=buttons)     

    if closed_cards == cards:
        await message.answer("ВЫ ВЫЙНРАЛИ!!! Для новой игры введите /start")


async def main() -> None:
    bot = Bot(token=TOKEN)

    await dp.start_polling(bot)


logging.basicConfig(level=logging.INFO)
asyncio.run(main())