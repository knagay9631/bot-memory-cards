from aiogram import F
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def create_game_keyboard(smiles_mitrix):
    print(smiles_mitrix)
    buttons_box = []

    for i in range(len(smiles_mitrix)):
        line = []
        for j in range(len(smiles_mitrix[i])):
            line.append(KeyboardButton(text=str(smiles_mitrix[i][j])))
        buttons_box.append(line)
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons_box,
        resize_keyboard=True
    )

    return keyboard