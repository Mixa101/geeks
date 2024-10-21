from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import db_main
from handlers import delete_products

# машина состояний для хранения индекса товара
class ProductState(StatesGroup):
    index = State()
    
# не забываем про DRY. XD
def making_caption(product : dict):
    caption = (f"{product['id']}\nназвание: {product['name_product']}\n"
                f"Размер : {product['size']}\n"
                f"Цена : {product['price']}\n"
                f"категория : {product['category']}\n"
                f"уникальное значение : {product['product_id']}\n"
                f"информация : {product['info_product']}\n"
                f"коллекция : {product['collection']}\n")
    return caption
# обработчик начала вывода
async def start_send_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    button_all = types.InlineKeyboardButton('вывести все товары', callback_data='all')
    button_one = types.InlineKeyboardButton('Вывести по одному', callback_data='one')
    keyboard.add(button_all, button_one)
    
    await message.answer("выберите как отправяться товары: ", reply_markup=keyboard)

# Выводим все что есть в базе данных по кнопке 'all'
async def sendall_products(call : types.CallbackQuery):
    products = db_main.fetch_all_products() # получаем данны из БД
    if products: # проверяем не пустая ли наша БД
        for product in products: # Используя цикл выводим все что мы получили
            caption = making_caption(product)
            delete_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
            delete_button = types.InlineKeyboardButton('Удалить', callback_data=f'delete_{product["product_id"]}')
            delete_keyboard.add(delete_button)
            
            await call.message.answer_photo(photo=product['photo'], caption=caption, reply_markup=delete_keyboard)
    # если наша БД пустая 
    else:
        await call.message.answer('Товаров нет')

# обработчик кнопки вывода по одной
async def send_one_product(call : types.CallbackQuery, state : FSMContext):
    products = db_main.fetch_all_products() # здесь тоже самое получаем данные из БД и т.д
    if products:
        await ProductState.index.set()
        async with state.proxy() as data:
            data['products'] = products # сохраняем в кэш наши данные
            data['index'] = 0 # сохраняем в кэш индекс
            
        product = products[data['index']]
        caption = making_caption(product)
        
        keyboard = types.InlineKeyboardMarkup(row_width=2 ,resize_keyboard = True)
        delete_button = types.InlineKeyboardButton('Удалить', callback_data=f'delete_{product["product_id"]}')
        next_button = types.InlineKeyboardButton('Следующий', callback_data='next')
        cancel_btn = types.InlineKeyboardButton('Отмена', callback_data='cancel')
        keyboard.add(next_button)
        keyboard.add(delete_button, cancel_btn)
        
        await call.message.answer_photo(photo=product['photo'], caption=caption, reply_markup=keyboard)
    else:
        await call.message.answer("Данных нет!")

# обработчик кнопки следующий для перехода на следующий товар
async def next_product(call : types.CallbackQuery, state : FSMContext):
    data = await state.get_data() # получаем наш кэш
    current_index = data['index']
    product = data['products'][current_index]
    # проверяем есть ли следующий элемент или это конец списка
    if current_index < len(data['products']) - 1:
        current_index += 1 # увеливаем индекс для перехода на следующий товар
        await state.update_data(index = current_index) # обновляем данные для кэша чтобы корректно работало
    else: # если это конец списка
        last_kb = types.InlineKeyboardMarkup(resize_keyboard = True)
        prev_button = types.InlineKeyboardButton('Прошлый', callback_data='back')
        delete_button = types.InlineKeyboardButton('Удалить', callback_data=f'delete_{product["product_id"]}')
        cancel_btn = types.InlineKeyboardButton('Отмена', callback_data='cancel')
        last_kb.add(prev_button, delete_button, cancel_btn)
        await call.message.edit_caption("Это был последний!", reply_markup=last_kb)
        return
    
    product = data['products'][current_index]
    keyboard = types.InlineKeyboardMarkup(row_width=2 ,resize_keyboard = True)
    next_button = types.InlineKeyboardButton('Следующий', callback_data='next')
    delete_button = types.InlineKeyboardButton('Удалить', callback_data=f'delete_{product["product_id"]}')
    cancel_btn = types.InlineKeyboardButton('Отмена', callback_data='cancel')
    back_button = types.InlineKeyboardButton('Прошлый', callback_data='back')
    keyboard.add(back_button, next_button, delete_button, cancel_btn)

    caption = making_caption(product)
    await call.message.edit_media(types.InputMediaPhoto(media=product['photo'], caption=caption), reply_markup=keyboard)

# обработчик кнопки прошлый здесь почти то же самое что в кнопке следующий единственное отличие в условий
async def prev_product(call : types.CallbackQuery, state : FSMContext):
    data = await state.get_data()
    current_index = data['index']
    product = data['products'][current_index]
    if current_index == 0:
        first_kb = types.InlineKeyboardMarkup(resize_keyboard = True)
        next_button = types.InlineKeyboardButton('Следующий', callback_data='next')
        delete_button = types.InlineKeyboardButton('Удалить', callback_data=f'delete_{product["product_id"]}')
        cancel_btn = types.InlineKeyboardButton('Отмена', callback_data='cancel')
        first_kb.add(delete_button, next_button, cancel_btn)
        await call.message.edit_caption('Это самый первый', reply_markup=first_kb)
        return
    current_index -= 1
    await state.update_data(index = current_index)
    product = data['products'][current_index]
    keyboard = types.InlineKeyboardMarkup(row_width=2 ,resize_keyboard = True)
    next_button = types.InlineKeyboardButton('Следующий', callback_data='next')
    delete_button = types.InlineKeyboardButton('Удалить', callback_data=f'delete_{product["product_id"]}')
    back_button = types.InlineKeyboardButton('Прошлый', callback_data='back')
    cancel_btn = types.InlineKeyboardButton('Отмена', callback_data='cancel')
    keyboard.add(back_button, next_button, delete_button, cancel_btn)
    caption = making_caption(product)

    await call.message.edit_media(types.InputMediaPhoto(media=product['photo'], caption=caption), reply_markup=keyboard)

# кнопка отмены для выхода из состояния
async def cancel_handler(call : types.CallbackQuery, state : FSMContext):
    await state.finish()
    await call.message.answer("Отменено!")
    
def register_send_products_handler(dp : Dispatcher):
    dp.register_message_handler(start_send_products, commands=['products'])
    dp.register_callback_query_handler(sendall_products, Text(equals='all'))
    dp.register_callback_query_handler(send_one_product, Text(equals='one'))
    dp.register_callback_query_handler(next_product, Text(equals='next'), state=ProductState.index)
    dp.register_callback_query_handler(prev_product, Text(equals='back'), state=ProductState.index)
    dp.register_callback_query_handler(delete_products.delete_product_callback, Text(startswith='delete_'), state='*')
    dp.register_callback_query_handler(cancel_handler, Text(equals='cancel'), state='*')
