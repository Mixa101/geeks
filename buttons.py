from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel = ReplyKeyboardMarkup(resize_keyboard=True)

cancel_button = KeyboardButton('Отмена')
cancel.add(cancel_button)

sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
size_buttons = [KeyboardButton(text=i) for i in sizes]
sizes_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

for i in range(0, len(sizes), 3):
    sizes_keyboard.add(size_buttons[i], size_buttons[i+1], size_buttons[i+3])
