import asyncio
import logging
import random

import buttons_factory
from constants import (
    OPEN_CARD_PLEASE, 
    CARD_OPEN, 
    USER_CARDS_COORD,
    WIN, 
    CLOSED_CARDS,
    LUCKI_NOT_WIN
)

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram import F


data = ''
with open("xc.txt", "r") as f:
    data = f.read()

TOKEN = data
dp = Dispatcher(storage=MemoryStorage())

line_1 = ["😊", "😫", "💋", "🦹🏼‍♂"]
line_2 = ["😎", "😇", "🥳", "🤣"]
line_3 = ["😊", "😫", "💋", "🦹🏼‍♂"]
line_4 = ["😎", "😇", "🥳", "🤣"]
random.shuffle(line_1)
random.shuffle(line_2)
random.shuffle(line_3)
random.shuffle(line_4)
cards = [ line_1, line_2, line_3, line_4 ]
random.shuffle(cards)


@dp.message(CommandStart())
async def command_start_handler(message:Message, state:FSMContext) -> None:
    buttons = buttons_factory.create_game_keyboard(CLOSED_CARDS)
    await state.clear()
    await state.set_data({"closed_cards": CLOSED_CARDS, "cards": cards, "user_cards_coord": USER_CARDS_COORD})
    await message.answer(f"Hello {message.from_user.full_name} :)", reply_markup=buttons)


@dp.message()
async def echo_handler(message:Message, state:FSMContext):
    data = await state.get_data()
    closed_cards = data["closed_cards"]
    cards = data["cards"]
    user_cards_coord = data["user_cards_coord"]
    output_message = ""

    if closed_cards == cards:
        return

    isCardFounded = False
    for line in closed_cards:
        if message.text in line:
            isCardFounded = True
    
    if not isCardFounded:
        output_message = OPEN_CARD_PLEASE
        return
    
    coord = message.text
    if not coord.isdigit():
        return
    
    if len(user_cards_coord) > 1:
        if closed_cards[user_cards_coord[0][0]][user_cards_coord[0][1]] == closed_cards[user_cards_coord[1][0]][user_cards_coord[1][1]]:
            user_cards_coord = []
            output_message = LUCKI_NOT_WIN
        else:
            closed_cards[user_cards_coord[0][0]][user_cards_coord[0][1]] = str(user_cards_coord[0][0]) + str(user_cards_coord[0][1])
            closed_cards[user_cards_coord[1][0]][user_cards_coord[1][1]] = str(user_cards_coord[1][0]) + str(user_cards_coord[1][1])
            user_cards_coord = []
    
    first_card_x = int(coord[0])
    first_card_y = int(coord[1])
    user_cards_coord.append([first_card_x, first_card_y])
    closed_cards[first_card_x][first_card_y] = cards[first_card_x][first_card_y]
    
    buttons = buttons_factory.create_game_keyboard(closed_cards)
    output_message = CARD_OPEN

    if closed_cards == cards:
        output_message = WIN

    await state.set_data({"closed_cards": closed_cards, "cards": cards, "user_cards_coord": user_cards_coord})
    await message.answer(output_message, reply_markup=buttons)

async def main() -> None:
    bot = Bot(token=TOKEN)

    await dp.start_polling(bot)

logging.basicConfig(level=logging.INFO)
asyncio.run(main())