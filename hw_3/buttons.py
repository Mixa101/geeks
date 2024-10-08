from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
size_buttons = [KeyboardButton(text=i) for i in sizes]
sizes_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

for i in range(0, len(sizes), 3):
    sizes_keyboard.add(size_buttons[i], size_buttons[i+1], size_buttons[i+2])

cancel = ReplyKeyboardMarkup(resize_keyboard=True)

cancel_button = KeyboardButton('Отмена')
cancel.add(cancel_button)

yes_or_no = ReplyKeyboardMarkup(resize_keyboard=True)
yes_or_no_buttons = [KeyboardButton(text='Да'), KeyboardButton(text='Нет')]
yes_or_no.add(yes_or_no_buttons[0], yes_or_no_buttons[1])
