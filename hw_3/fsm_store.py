from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from buttons import sizes_keyboard, sizes, cancel, yes_or_no

class fsm_store(StatesGroup):
    product_name = State()
    size = State()
    category = State()
    price = State()
    photo = State()
    data_correction = State()
    
async def cancel_fsm(message : types.Message, state: FSMContext):
    if await state.get_state() is not None:
        await state.finish()
        await message.answer("Отменено", reply_markup=ReplyKeyboardRemove())
        
async def start_product(message : types.Message):
    await message.answer("введите название товара:", reply_markup = cancel)
    await fsm_store.product_name.set()

async def load_product_name(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['product_name'] = message.text
    await message.answer("Введите нужный размер:", reply_markup=sizes_keyboard)
    await fsm_store.next()

async def load_size(message : types.Message, state : FSMContext):
    if message.text in sizes:
        async with state.proxy() as data:
            data['size'] = message.text
        await message.answer("Выберите категорию:", reply_markup=cancel)
        await fsm_store.next()
    else:
        await message.answer(f"У нас нет такого размера!\n"
                            "выберите из кнопки!", reply_markup=sizes_keyboard)


async def load_category(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    
    await message.answer("Введите цену:")
    await fsm_store.next()

async def load_price(message : types.Message, state : FSMContext):
    if message.text.isnumeric():
        async with state.proxy() as data:
            data['price'] = message.text
    
        await message.answer("Фото товара: ")
        await fsm_store.next()
    else:
        await message.answer("Цена должна состоять из цифр!")

async def load_photo(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    
    await message.answer_photo(photo=data["photo"],
                            caption=f'Ваш товар:\n'
                            f'Название товара: {data["product_name"]}\n'
                            f'Размер: {data["size"]}\n'
                            f'Категория: {data["category"]}\n'
                            f'Цена: {data["price"]}\n',
                            reply_markup=ReplyKeyboardRemove())
    await message.answer("Все верно?", reply_markup=yes_or_no)
    await fsm_store.next()

async def correct_data(message : types.Message, state : FSMContext):
    if message.text.lower() == 'да':
        await message.answer('Сохранено в базу', reply_markup=ReplyKeyboardRemove())
        await state.finish()
    elif message.text.lower() == 'нет':
        await message.answer("Бери что есть!", reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer("не понял 'да' или 'нет'?", reply_markup=yes_or_no)
        
def register_store_handlers(dp : Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals="Отмена", ignore_case=True),state='*')
    dp.register_message_handler(start_product, commands=['store'])
    dp.register_message_handler(load_product_name, state=fsm_store.product_name)
    dp.register_message_handler(load_size, state=fsm_store.size)
    dp.register_message_handler(load_category, state=fsm_store.category)
    dp.register_message_handler(load_price, state=fsm_store.price)
    dp.register_message_handler(load_photo, state=fsm_store.photo, content_types=['photo'])
    dp.register_message_handler(correct_data, state=fsm_store.data_correction)