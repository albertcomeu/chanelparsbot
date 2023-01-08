import aiogram
from telethon import TelegramClient, events, sync
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

app_id = ###########################
app_hash = ##########################
phone = ###########################

client = TelegramClient(phone, app_id, app_hash)
client.connect()

chanellist = []
filterlist = []
chanelstopost = []


if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('code: '))

token = ########################
bot = aiogram.Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())


class ChanelPost(StatesGroup):
    chanelpostname = State()

class DelChanelPost(StatesGroup):
    delchanelname = State()

class ChanelForm(StatesGroup):
    chanelname = State()


class FilterForm(StatesGroup):
    filtername = State()

class DelFilterForm(StatesGroup):
    delfilter = State()


class DelForm(StatesGroup):
    delname = State()


class PostForm(StatesGroup):
    post = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global flag
    global chanellist
    global filterlist
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton('Изменить список каналов')
    b2 = types.KeyboardButton('Изменить фильтры')
    b3 = types.KeyboardButton('Выложить пост')
    b4 = types.KeyboardButton('Изменить каналы для постинга')
    markup.add(b1, b2, b3, b4)

    f = open('chanels.txt', 'r')

    chanellist1 = f.readlines()
    chanellist1 = list(map(lambda x: str(x.strip('\n')), chanellist1))
    chanellist = []
    for i in chanellist1:
        if (i) and (i not in ('\n')):
            chanellist.append(int(i))

    print('список каналов', chanellist)
    f.close()

    f = open('filter.txt', 'r', encoding='cp1251')
    filterlist1 = f.readlines()
    filterlist1 = list(map(lambda x: str(x.strip('\n')), filterlist1))
    filterlist = []
    for i in filterlist1:
        if (i) and (i not in ('\n')):
            filterlist.append(i)
    f.close()
    print('список фильтров', filterlist)

    f = open('getmessage.txt', 'r')
    check1 = f.readlines()
    check1 = list(map(lambda x: str(x.strip('\n')), check1))
    check = []
    for i in check1:
        if (i) and (i not in ('\n')):
            check.append(i)

    f = open('getmessage.txt', 'a')
    if str(message.from_id) not in check:
        f.write(str(message.from_id) + '\n')
    f.close()

    print('список пользователей', check)

    await bot.send_message(message.chat.id, text='что нужно сделать?', reply_markup=markup)



async def botstart():
    await dp.start_polling(bot)


async def clientstart():
    await client.run_until_disconnected()


@dp.message_handler(lambda message: message.text == 'Выложить пост')
async def new_post(message):
    await bot.send_message(message.chat.id, text='Перешлите сюда пост который хотите выложить')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton('Отмена')
    markup.add(b1)
    await bot.send_message(message.chat.id, text='нажмите кнопку для отмены', reply_markup=markup)

    await PostForm.post.set()

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
async def cancel(message: types.Message, state: FSMContext):
    curs = await state.get_state()
    if curs is None:
        return

    await state.finish()
    await message.answer('отменяю')
    await start(message)

@dp.message_handler(state=PostForm.post, content_types=['any'])
async def new_post2(message: types, state=FSMContext):
    await state.finish()
    global chanelstopost
    f = open('postchnels.txt', 'r')
    chanelstopost1 = f.readlines()
    chanelstopost1 = list(map(lambda x: str(x.strip('\n')), chanelstopost1))
    chanelstopost = []

    for i in chanelstopost1:
        if (i) and (i not in ('\n')):
            chanelstopost.append(i)
    f.close()
    print('каналы для постинга', chanelstopost)

    for i in chanelstopost:
        i = '-100' + i
        print(i)
        await bot.copy_message(chat_id=i, from_chat_id=message.chat.id, message_id=message.message_id)

    await start(message)


#Парсинг
@client.on(events.NewMessage())
async def pars(event):
    try:
        if event.message.peer_id.channel_id in chanellist:
            if filter(str(event.message.text)):
                print('to testchnel', event.message)
                await client.forward_messages(int('-100' + str(1878355518)), event.message)
                m = await client.get_messages(int('-100' + str(1878355518)), limit=1)
                f = open('getmessage.txt', 'r')
                getlist = f.readlines()
                getlist = list(map(lambda x: str(x.strip('\n')), getlist))
                f.close()
                print(getlist)
                for i in getlist:
                    await bot.forward_message(chat_id=i, from_chat_id=-1001878355518, message_id=m[0].id)


    except:
        pass

def filter(messagetext):
    for i in filterlist:
        if i.lower() in messagetext.lower():
            return False
    return True


@dp.message_handler(lambda message: message.text == 'Назад')
async def returnto(message):
    await start(message)


@dp.message_handler(lambda message: message.text == 'Изменить каналы для постинга')
async def menu_postchanel_list(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    c1 = types.KeyboardButton('Добавить канал для постинга')
    c2 = types.KeyboardButton('Удалить канал для постинга')
    c3 = types.KeyboardButton('Вывести список каналов для постинга')
    c4 = types.KeyboardButton('Назад')

    markup.add(c1, c2, c3, c4)
    await bot.send_message(message.chat.id, text='что нужно сделать?', reply_markup=markup)

@dp.message_handler(lambda message: message.text == 'Добавить канал для постинга')
async def add_chanelpost(message):
    await bot.send_message(message.chat.id, text='Введите название канала')
    await ChanelPost.chanelpostname.set()


@dp.message_handler(state=ChanelPost.chanelpostname)
async def add_chanelpost2(message, state: FSMContext):
    async with state.proxy() as data:
        data['chanelpostname'] = message
        print(data['chanelpostname'])
        await state.finish()

    f = open('postchnels.txt', 'r')
    check = f.readlines()
    check = list(map(lambda x: str(x.strip('\n')), check))
    if str(message.text) not in check:
        f = open('postchnels.txt', 'a')
        f.write(str(message.text) + '\n')
        await bot.send_message(message.chat.id, text='Канал добавлен')

    else:
        await bot.send_message(message.chat.id, text='Канал уже есть в списке')

    f.close()

    await menu_postchanel_list(message)


@dp.message_handler(lambda message: message.text == 'Удалить канал для постинга')
async def del_postchanel(message):
    await bot.send_message(message.chat.id, text='Введите название канала')
    await DelChanelPost.delchanelname.set()


@dp.message_handler(state=DelChanelPost.delchanelname)
async def del_postchanel2(message, state: FSMContext):
    async with state.proxy() as data:
        data['delchanelname'] = message
        await state.finish()
    chanel2del = str(message.text)
    f = open('postchnels.txt', 'r')
    lines = f.readlines()

    if (chanel2del + '\n') not in lines:
        await bot.send_message(message.chat.id, text='Такого канала нет в списке')
        await menu_postchanel_list(message)

    else:
        f = open('postchnels.txt', 'w')
        for line in lines:
            if line.strip('\n') != chanel2del:
                f.write(line)
        f.close()

        await bot.send_message(message.chat.id, text='Канал удалён')
        await menu_postchanel_list(message)


@dp.message_handler(lambda message: message.text == 'Вывести список каналов для постинга')
async def print_postchanel(message):
    await bot.send_message(message.chat.id, text='Список каналов: ')
    f = open('postchnels.txt', 'r')
    for i in f:
        if i[:2] != '\n': await bot.send_message(message.chat.id, text=i)
    f.close()
    await menu_postchanel_list(message)
##########################################################################################
@dp.message_handler(lambda message: message.text == 'Изменить список каналов')
async def menu_chanel_list(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    c1 = types.KeyboardButton('Добавить канал')
    c2 = types.KeyboardButton('Удалить канал')
    c3 = types.KeyboardButton('Вывести список каналов')
    c4 = types.KeyboardButton('Назад')

    markup.add(c1, c2, c3, c4)
    await bot.send_message(message.chat.id, text='что нужно сделать?', reply_markup=markup)

@dp.message_handler(lambda message: message.text == 'Назад')
async def returnto(message):
    await start(message)


@dp.message_handler(lambda message: message.text == 'Добавить канал')
async def add_chanel(message):
    await bot.send_message(message.chat.id, text='Введите название канала')
    await ChanelForm.chanelname.set()


@dp.message_handler(state=ChanelForm.chanelname)
async def add_chanel2(message, state: FSMContext):
    async with state.proxy() as data:
        data['chanelname'] = message
        print(data['chanelname'])
        await state.finish()

    f = open('chanels.txt', 'r')
    check = f.readlines()
    check = list(map(lambda x: str(x.strip('\n')), check))

    if str(message.text) not in check:
        f = open('chanels.txt', 'a')
        f.write('\n' + str(message.text) + '\n')
        await bot.send_message(message.chat.id, text='Канал добавлен')

    else:
        await bot.send_message(message.chat.id, text='Канал уже есть в списке')

    f.close()

    await menu_chanel_list(message)


@dp.message_handler(lambda message: message.text == 'Удалить канал')
async def del_chanel(message):
    await bot.send_message(message.chat.id, text='Введите название канала')
    await DelForm.delname.set()


@dp.message_handler(state=DelForm.delname)
async def del_chanel2(message, state: FSMContext):
    async with state.proxy() as data:
        data['delname'] = message
        await state.finish()
    chanel2del = str(message.text)
    f = open('chanels.txt', 'r')
    lines = f.readlines()

    if (chanel2del + '\n') not in lines:
        await bot.send_message(message.chat.id, text='Такого канала нет в списке')
        await menu_chanel_list(message)

    else:
        f = open('chanels.txt', 'w')
        for line in lines:
            if line.strip('\n') != chanel2del:
                f.write(line)
        f.close()

        await bot.send_message(message.chat.id, text='Канал удалён')
        await menu_chanel_list(message)


@dp.message_handler(lambda message: message.text == 'Вывести список каналов')
async def print_chanel(message):
    await bot.send_message(message.chat.id, text='Список каналов: ')
    f = open('chanels.txt', 'r')
    for i in f:
        if i[:2] != '\n': await bot.send_message(message.chat.id, text=i)
    f.close()
    await menu_chanel_list(message)


#изменение фильтров
@dp.message_handler(lambda message: message.text == 'Изменить фильтры')
async def menu_filter_list(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    c1 = types.KeyboardButton('Добавить фильтр')
    c2 = types.KeyboardButton('Удалить фильтр')
    c3 = types.KeyboardButton('Вывести список фильтров')
    c4 = types.KeyboardButton('Назад')

    markup.add(c1, c2, c3, c4)
    await bot.send_message(message.chat.id, text='что нужно сделать?', reply_markup=markup)


@dp.message_handler(lambda message: message.text == 'Назад')
async def returnto(message):
    await start(message)


@dp.message_handler(lambda message: message.text == 'Добавить фильтр')
async def add_filter(message):
    await bot.send_message(message.chat.id, text='Введите фильтр')
    await FilterForm.filtername.set()


@dp.message_handler(state=FilterForm.filtername)
async def add_filter2(message, state: FSMContext):
    async with state.proxy() as data:
        data['filtername'] = message
        print(data['filtername'])
        await state.finish()

    f = open('filter.txt', 'r')
    check = f.readlines()
    check = list(map(lambda x: str(x.strip('\n')), check))

    if str(message.text) not in check:
        f = open('filter.txt', 'a')
        f.write(str(message.text) + '\n')
        f.close()
        await bot.send_message(message.chat.id, text='Фильтр добавлен')

    else:
        await bot.send_message(message.chat.id, text='Фильтр уже есть в списке')

    await menu_filter_list(message)


@dp.message_handler(lambda message: message.text == 'Удалить фильтр')
async def del_filter(message):
    await bot.send_message(message.chat.id, text='Введите фильтр')
    await DelFilterForm.delfilter.set()


@dp.message_handler(state=DelFilterForm.delfilter)
async def del_filter2(message, state: FSMContext):
    async with state.proxy() as data:
        data['delfilter'] = message
        await state.finish()
    filter2del = str(message.text)
    f = open('filter.txt', 'r')
    lines = f.readlines()

    if (filter2del + '\n') not in lines:
        await bot.send_message(message.chat.id, text='Такого фильтра нет в списке')
        await menu_filter_list(message)

    else:
        f = open('filter.txt', 'w')
        for line in lines:
            if line.strip('\n') != filter2del:
                f.write(line)
        f.close()

        await bot.send_message(message.chat.id, text='Фильтр удалён')
        await menu_filter_list(message)


@dp.message_handler(lambda message: message.text == 'Вывести список фильтров')
async def print_filter(message):
    await bot.send_message(message.chat.id, text='Список фильтров: ')
    f = open('filter.txt', 'r')
    for i in f:
        if i[:2] != '\n': await bot.send_message(message.chat.id, text=i)
    f.close()
    await menu_filter_list(message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(botstart())
    loop.create_task(clientstart())
    loop.run_until_complete(clientstart())
