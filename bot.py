# Imports

# Libs
import asyncio
import json

from aiogram import Bot, \
    Dispatcher, \
    types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import BotCommand

# Modules
import keyboards
from config import ReadConfig, ChangeConfig

# Configuring Bot and Dispatcher
bot = Bot(token=ReadConfig('SAFE', 'API_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())

# ChangeConfig('MESSAGES', 'faq',
# """
# I only wish to be helpful for someone:
# that's why I'm spending time on creating
# this bot instead of exam's preparation.
#
# Hope it will simplify your life.
#
# To be updated soon.
# """)

ChangeConfig('MESSAGES', 'faq', """
to be updated

""")


# *-* Code here *-*
class Menu(StatesGroup):
    none = State()
    default = State()
    faq = State()
    authors = State()
    contributing = State()
    cards = State()


class Cards(StatesGroup):
    removing_cards = State()
    adding_cards_answer_entered = State()
    adding_cards_question_entered = State()
    adding_cards = State()
    none = State()
    default = State()
    my = State()
    chosen = State()
    sureance = State()

    configuring = State()
    configuring_name = State()
    configuring_name_entered = State()
    configuring_description = State()
    configuring_description_entered = State()
    configuring_order = State()
    configuring_order_entered = State()

    created = State()
    named = State()
    descriptioned = State()
    editing_cards = State()

    add = State()


# ---------- Menu ---------- #

async def Start(message: types.Message):
    await message.answer(ReadConfig('MESSAGES', 'start'), reply_markup=keyboards.kb_menu)
    await Menu.default.set()

    import json

    with open("users.json", "r+") as file:
        data = json.load(file)
        users = [i for i in data]

        if (str(message.from_user.id)) in users:
            pass
        else:
            data[f"{message.from_user.id}"] = []
            file.seek(0)
            json.dump(data, file)


@dp.message_handler(text='Menu', state="*")
async def Menu_Cancel(message: types.Message,
                      state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text='Back to menu', reply_markup=keyboards.kb_menu)
    await Menu.default.set()
    await state.reset_data()


@dp.message_handler(text='FAQ', state=Menu.default)
async def FAQ(message: types.Message):
    await Menu.faq.set()
    await bot.send_message(chat_id=message.from_user.id, text=ReadConfig('MESSAGES', 'faq'),
                           reply_markup=keyboards.kb_menu)
    await Menu.default.set()


@dp.message_handler(text='Authors & Contributing', state=Menu.default)
async def AuthorsAndContributing(message: types.Message):
    await Menu.authors.set()
    await bot.send_message(chat_id=message.from_user.id, text=ReadConfig('MESSAGES', 'authors'),
                           reply_markup=keyboards.kb_menu)
    await Menu.contributing.set()
    await bot.send_message(chat_id=message.from_user.id, text=ReadConfig('MESSAGES', 'contributing'),
                           reply_markup=keyboards.kb_menu)
    await Menu.default.set()


# ---------- Cards ---------- #

# ----- Common -----

@dp.message_handler(text='Cards', state=[Menu.default, Cards.descriptioned])
async def Decks1(message: types.Message):
    await Cards.default.set()

    import json

    with open('users.json', 'r+') as file:
        data = json.load(file)

    # Если я зареган - норм, выдать клавиатуру
    if any(i == f'{message.from_user.id}' for i in data):
        # Если есть колоды
        if len(data[f'{message.from_user.id}']) > 0:
            await bot.send_message(chat_id=message.from_user.id, text='you have cards',
                                   reply_markup=keyboards.kb_have_cards)


        # Если нет колод
        else:
            await bot.send_message(chat_id=message.from_user.id, text='you dont have cards',
                                   reply_markup=keyboards.kb_dont_have_cards)

    # Если я не зареган - хуево
    else:
        import json

        with open("users.json", "r+") as file:
            data = json.load(file)
            users = [i for i in data]

        # Зарегать
        data[f"{message.from_user.id}"] = []
        with open("users.json", "w") as file:
            json.dump(data, file)

        # Выдать клавиатуру
        # Если есть колоды
        if len(data[f'{message.from_user.id}']) > 0:
            await bot.send_message(chat_id=message.from_user.id, text='you have cards',
                                   reply_markup=keyboards.kb_have_cards)


        # Если нет колод
        else:
            await bot.send_message(chat_id=message.from_user.id, text='you dont have cards',
                                   reply_markup=keyboards.kb_dont_have_cards)


# Есть колоды - кнопка MY CARDS
@dp.message_handler(text='My cards', state=Cards.default)
async def MyDecks(message: types.Message, state: FSMContext):
    await Cards.my.set()

    with open('users.json', 'r') as file:
        data = json.load(file)
        decks_arr = [i for i in data[f'{message.from_user.id}']]
        # print(decks_arr)

        await state.update_data(decks_arr=decks_arr)

    # Предложить выбрать колоду, нажать на "/название"
    with open('cards.json', 'r') as file:
        data = json.load(file)

        # await bot.send_message(chat_id=message.from_user.id, text='Please, choose the deck:\nTap on a / number',
        #                       reply_markup=keyboards.kb_cancel)

        counter = 1
        output = 'Please, choose the deck:\nTap on a / number\n\n'
        for deck in decks_arr:
            output += f"/{counter} - {data[deck]['name']}\n"
            counter += 1
        await bot.send_message(chat_id=message.from_user.id,
                               text=output,
                               reply_markup=keyboards.kb_cancel)


# Выбор колоды
@dp.message_handler(state=Cards.my)
async def ChoosingTheDeck(message: types.Message, state: FSMContext):
    await Cards.chosen.set()

    order = str(message.get_command())

    # если ответ пользователя содержит /
    if order[0] == '/':
        order = order.lstrip('/')

        userdata = await state.get_data()

        # если ответ пользователя формата /номер_колоды
        if order.isdigit():

            # если колода с таким номером НЕ существует
            if int(order) > len(userdata['decks_arr']):
                await bot.send_message(chat_id=message.from_user.id, text=f'Choose the correct answer with / *number*')
                await Cards.my.set()

            # если колода с таким номером СУЩЕСТВУЕТ
            else:

                # обновляю state["deck_id"]
                await state.update_data(deck_id=userdata['decks_arr'][int(order) - 1])
                userdata = await state.get_data()

                with open('cards.json', 'r') as file:
                    datas = json.load(file)
                    # обновляю state["deck_name"]
                    await state.update_data(deck_name=datas[f'{userdata["deck_id"]}']['name'])

                # Получаю текущее содержание состояния
                userdata = await state.get_data()

                # Вывести название колоды и клавиатуру с операциями
                await bot.send_message(chat_id=message.from_user.id, text=f'{userdata["deck_name"]}:',
                                       reply_markup=keyboards.kb_deckactions)

        else:
            await bot.send_message(chat_id=message.from_user.id, text=f'Choose the correct answer with / *number*')
            await Cards.my.set()

    else:
        await bot.send_message(chat_id=message.from_user.id, text=f'Choose the correct answer with / *number*')
        await Cards.my.set()


# Удаление колоды
@dp.message_handler(text='Delete', state=Cards.chosen)
async def DeckDelete(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Are you sure?', reply_markup=keyboards.kb_sure)
    await Cards.sureance.set()


# Конфигурация колоды
@dp.message_handler(text='Configure', state=Cards.chosen)
async def DeckConfigure(message: types.Message, state: FSMContext):
    userdata = await state.get_data()

    # Если я владелец
    if str(message.from_user.id) in userdata['deck_id']:
        await bot.send_message(chat_id=message.from_user.id, text='You are the owner')

        await Cards.configuring.set()

        with open('cards.json', 'r') as file:
            data = json.load(file)

        name = data[f'{userdata[f"deck_id"]}']['name']
        description = data[f'{userdata[f"deck_id"]}']['description']
        order = data[f'{userdata[f"deck_id"]}']['order']
        await state.update_data(deck_order=order)

        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Name: {name}\nDescription: {description}\nOrder: {order}',
                               reply_markup=keyboards.kb_configuring)


    # Если я не владелец
    else:
        await Cards.default.set()
        with open('users.json', 'r+') as file:
            data = json.load(file)

        await bot.send_message(chat_id=message.from_user.id, text=f"Sorry, you can't configure this deck")
        # Если есть колоды
        if len(data[f'{message.from_user.id}']) > 0:
            await bot.send_message(chat_id=message.from_user.id, text='you have cards',
                                   reply_markup=keyboards.kb_have_cards)


        # Если нет колод
        else:
            await bot.send_message(chat_id=message.from_user.id, text='you dont have cards',
                                   reply_markup=keyboards.kb_dont_have_cards)


@dp.message_handler(text='Name', state=Cards.configuring)
async def ConfiguringName(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Enter the name you want',
                           reply_markup=keyboards.kb_cancel)
    await Cards.configuring_name.set()


@dp.message_handler(state=Cards.configuring_name)
async def ConfiguringNameEntered(message: types.Message, state: FSMContext):
    await Cards.configuring_name_entered.set()
    await state.update_data(name_to_change=message.text)

    userdata = await state.get_data()
    with open('cards.json', 'r') as file:
        data = json.load(file)

    data[f'{userdata[f"deck_id"]}']["name"] = userdata['name_to_change']
    with open('cards.json', 'w') as file:
        json.dump(data, file)

    await bot.send_message(chat_id=message.from_user.id, text='Name changed', reply_markup=keyboards.kb_have_cards)
    await Menu.default.set()

    with open('users.json', 'r+') as file:
        data = json.load(file)

    if len(data[f'{message.from_user.id}']) > 0:
        await bot.send_message(chat_id=message.from_user.id, text='you have cards')
        await Cards.default.set()


    # Если нет колод
    else:
        await bot.send_message(chat_id=message.from_user.id, text='you dont have cards',
                               reply_markup=keyboards.kb_dont_have_cards)
        await Cards.default.set()


@dp.message_handler(text='Description', state=Cards.configuring)
async def ConfiguringDescription(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Enter the description you want',
                           reply_markup=keyboards.kb_cancel)
    await Cards.configuring_description.set()


@dp.message_handler(state=Cards.configuring_description)
async def ConfiguringDescriptionEntered(message: types.Message, state: FSMContext):
    await Cards.configuring_description_entered.set()
    await state.update_data(description_to_change=message.text)

    state_data = await state.get_data()
    with open('cards.json', 'r') as file:
        data = json.load(file)

    data[f'{state_data[f"deck_id"]}']["description"] = state_data['description_to_change']
    with open('cards.json', 'w') as file:
        json.dump(data, file)

    await bot.send_message(chat_id=message.from_user.id, text='Description changed')

    with open('users.json', 'r') as file:
        data = json.load(file)

    # если есть колоды
    if len(data[f'{message.from_user.id}']) > 0:
        await bot.send_message(chat_id=message.from_user.id, text='you have cards',
                               reply_markup=keyboards.kb_have_cards)


    # Если нет колод
    else:
        await bot.send_message(chat_id=message.from_user.id, text='you dont have cards',
                               reply_markup=keyboards.kb_dont_have_cards)

    await Cards.default.set()


@dp.message_handler(text='Order', state=Cards.configuring)
async def ConfiguringOrder(message: types.Message):
    await Cards.configuring_order.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Choose the mode to set',
                           reply_markup=keyboards.kb_order)


@dp.message_handler(state=Cards.configuring_order)
async def ConfiguringOrderEntered(message: types.Message, state: FSMContext):
    await Cards.configuring_order_entered.set()

    if message.text == 'Straight' or message.text == 'Reversed' or message.text == 'Random':
        await state.update_data(order_to_change=message.text)
        userdata = await state.get_data()

        with open('cards.json', 'r') as file:
            data = json.load(file)

        data[f'{userdata[f"deck_id"]}']["order"] = userdata['order_to_change']
        with open('cards.json', 'w') as file:
            json.dump(data, file)

        await bot.send_message(chat_id=message.from_user.id, text='Order changed')
        await Cards.default.set()

        with open('users.json', 'r') as file:
            data = json.load(file)

        # если есть колоды
        if len(data[f'{message.from_user.id}']) > 0:
            await bot.send_message(chat_id=message.from_user.id, text='you have cards',
                                   reply_markup=keyboards.kb_have_cards)


        # Если нет колод
        else:
            await bot.send_message(chat_id=message.from_user.id, text='you dont have cards',
                                   reply_markup=keyboards.kb_dont_have_cards)

        await Cards.default.set()
    else:
        await bot.send_message(chat_id=message.from_user.id, text='Choose the mode with keyboard')
        await Cards.configuring_order.set()


@dp.message_handler(text='Sure', state=Cards.sureance)
async def DeckDeleteSure(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    # Открыть users.json, удалить выбранную колоду у юзера
    with open('users.json', 'r+') as file:
        data = json.load(file)
        decks = data[f'{message.from_user.id}']
        decks.remove(f'{state_data["deck_id"]}')
        data[f'{message.from_user.id}'] = decks

    # Перезаписать файл
    with open('users.json', 'w') as file:
        json.dump(data, file)

    await bot.send_message(chat_id=message.from_user.id, text='Deleted')

    # Если есть колоды
    if len(data[f'{message.from_user.id}']) > 0:
        await bot.send_message(chat_id=message.from_user.id, text='you have decks',
                               reply_markup=keyboards.kb_have_cards)


    # Если нет колод
    else:
        await bot.send_message(chat_id=message.from_user.id, text='you dont have decks',
                               reply_markup=keyboards.kb_dont_have_cards)

    await Cards.default.set()


@dp.message_handler(text='Unsure', state=Cards.sureance)
async def DeckDeleteUnsure(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Not deleted',
                           reply_markup=keyboards.kb_deckactions)

    await Cards.chosen.set()


@dp.message_handler(text='Back', state=Cards.configuring)
async def ConfiguringBackToCardChosen(message: types.Message, state: FSMContext):
    await Cards.chosen.set()

    userdata = await state.get_data()

    with open('cards.json', 'r') as file:
        datas = json.load(file)
        # обновляю state["deck_name"]
        await state.update_data(deck_name=datas[f'{userdata["deck_id"]}']['name'])

    # Получаю текущее содержание состояния
    userdata = await state.get_data()

    # Вывести название колоды и клавиатуру с операциями
    await bot.send_message(chat_id=message.from_user.id, text=f'{userdata["deck_name"]}:',
                           reply_markup=keyboards.kb_deckactions)


# ----- Creating ----- #
@dp.message_handler(text='Create own', state=Cards.default)
async def CardsCreate(message: types.Message):
    await Cards.created.set()
    await bot.send_message(chat_id=message.from_user.id, text='Enter the name', reply_markup=keyboards.kb_cancel)


@dp.message_handler(state=Cards.created)
async def CardsNamed(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await bot.send_message(chat_id=message.from_user.id, text='Enter the description', reply_markup=keyboards.kb_cancel)
    await Cards.named.set()


@dp.message_handler(state=Cards.named)
async def CardsDescriptioned(message: types.Message, state: FSMContext):
    await state.update_data(deck_description=message.text)
    await bot.send_message(chat_id=message.from_user.id, text='The deck was created',
                           reply_markup=keyboards.kb_deckcreated)
    await Cards.descriptioned.set()

    userdata = await state.get_data()

    import json
    import csv

    # Добавление колоды в users.json и формирование переменных
    with open('users.json', 'r+') as file:
        data = json.load(file)
        decks_array = data[f'{message.from_user.id}']
        decks_counter = len(decks_array)
        deck_id = (str(message.from_user.id) + f'_{decks_counter + 1}')
        (data[f'{message.from_user.id}']).append(deck_id)
        file.seek(0)
        json.dump(data, file)

    # def Default():
    #     data = {
    #         f"{deck_name}": {
    #             "name": f"{state_data['name']}",
    #             "description": f"{state_data['deck_description']}",
    #             "order": "0"
    #         }
    #     }
    #
    #     with open('cards.json', 'r+') as file:
    #         json.dump(data, file)

    # Добавление колоды в cards.json
    with open('cards.json', 'r+') as file:
        data = json.load(file)
        data[f'{deck_id}'] = {
            "name": f"{userdata['name']}",
            "description": f"{userdata['deck_description']}",
            "order": "Straight"}

    with open('cards.json', 'w') as file:
        json.dump(data, file)

    await state.update_data(deck_id=deck_id)
    userdata = await state.get_data()

    # Создать .CSV файл колоды с соответсвующим именем
    with open(f'./{userdata["deck_id"]}.csv', 'w') as file:
        csv_writer = csv.writer(file, delimiter='|')
        csv_writer.writerow(['Question', 'Answer'])
# --- Editing --- #
@dp.message_handler(text='Edit cards', state=[Cards.descriptioned, Cards.chosen])
async def EditingCards(message: types.Message, state: FSMContext):
    import csv
    await Cards.editing_cards.set()
    await bot.send_message(chat_id=message.from_user.id, text='Editing cards')

    userdata = await state.get_data()
    # with open(f'./{name}.csv', 'a') as file:
    #     csv_writer = csv.writer(file)
    #
    #     csv_writer.writerow([f"{userdata['name']}", f"{userdata['description']}", f"{message.from_user.id}"])
    #
    #
    with open(f'./{userdata["deck_id"]}.csv', 'r') as file:
        csv_reader = csv.reader(file)

        datas = [line for line in csv_reader]
        datas.pop(0)

    # если в колоде ничего нет
    if len(datas) == 1 and len(datas[0]) == 0:
        await bot.send_message(chat_id=message.from_user.id,
                               text='The deck is empty',
                               reply_markup=keyboards.kb_editing)
        await state.update_data(contain=False)
    # если в колоде есть карты
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='The deck is NOT empty',
                               reply_markup=keyboards.kb_editing)
        await state.update_data(contain=True)

    userdata = await state.get_data()
    # print(userdata)


@dp.message_handler(text='Add', state=[Cards.editing_cards])
async def AddingCards(message: types.Message, state: FSMContext):
    await Cards.adding_cards.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Please enter the question\n"
                                "Don't use '|' symbol",
                           reply_markup=keyboards.kb_cancel)


@dp.message_handler(state=Cards.adding_cards)
async def AddingCardsQuestionEntered(message: types.Message,
                                     state: FSMContext):
    question = message.text
    if '|' in question:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Please enter the QUESTION\n"
                                    "Don't use '|' symbol",
                               reply_markup=keyboards.kb_cancel)
    else:
        await Cards.adding_cards_question_entered.set()
        await state.update_data(question=message.text)
        await bot.send_message(chat_id=message.from_user.id,
                               text="Please enter the ANSWER\n"
                                    "Don't use '|' symbol",
                               reply_markup=keyboards.kb_cancel)


@dp.message_handler(state=Cards.adding_cards_question_entered)
async def AddingCardsQuestionEntered(message: types.Message,
                                     state: FSMContext):
    answer = message.text
    if '|' in answer:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Please enter the ANSWER\n"
                                    "Don't use '|' symbol",
                               reply_markup=keyboards.kb_cancel)
    else:
        await Cards.adding_cards_answer_entered.set()
        await state.update_data(answer=message.text)
        await bot.send_message(chat_id=message.from_user.id,
                               text="Card added",
                               reply_markup=keyboards.kb_editing)
        await Cards.editing_cards.set()

    userdata = await state.get_data()

    import csv

    with open(f'./{userdata["deck_id"]}.csv') as file:
        reader = csv.DictReader(file,
                                delimiter='|')
        result = []
        for row in reader:
            result.append(row)
        result.append({"question": f"{userdata['question']}", "answer": f"{userdata['answer']}"})

    with open(f'./{userdata["deck_id"]}.csv', 'w', newline='') as file:
        fieldnames = ['question', 'answer']
        writer = csv.DictWriter(file,
                                fieldnames=fieldnames,
                                delimiter='|')
        writer.writeheader()

        for row in result:
            writer.writerow(row)


@dp.message_handler(text='Show', state=Cards.editing_cards)
async def EditingCardsShow(message: types.message,
                           state: FSMContext):
    import csv
    userdata = await state.get_data()

    with open(f'./{userdata["deck_id"]}.csv') as file:
        reader = csv.DictReader(file, delimiter='|')
        output = ''
        counter = 1
        for row in reader:
            output += f"{counter})\n" + f"--- {row['question']}\n" + f"--- {row['answer']}\n\n"
            counter += 1

        await bot.send_message(chat_id=message.from_user.id,
                               text=output,
                               reply_markup=keyboards.kb_editing)

@dp.message_handler(text='Play',state=Cards.chosen)
async def PlayingCards(message: types.Message,
                       state: FSMContext):
    userdata = await state.get_data()
    with open('cards.json', 'r') as file:
        data = json.load(file)
    name = (data[f'{userdata["deck_id"]}'])['name']
    description = (data[f'{userdata["deck_id"]}'])['description']
    order = (data[f'{userdata["deck_id"]}'])['order']
    print(name,description, order)

# Удалить карту - список карт на удаление
@dp.message_handler(text='Remove', state=Cards.editing_cards)
async def EditingCardsRemove(message: types.message,
                             state: FSMContext):
    import csv
    await Cards.removing_cards.set()
    userdata = await state.get_data()

    with open(f'./{userdata["deck_id"]}.csv') as file:
        reader = csv.DictReader(file, delimiter='|')
        output = 'Please, choose the card:\n' \
                 'Tap on a / number\n\n'
        counter = 1
        for row in reader:
            output += f"/{counter}\n" + f"--- {row['question']}\n" + f"--- {row['answer']}\n\n"
            counter += 1

        await bot.send_message(chat_id=message.from_user.id,
                               text=output,
                               reply_markup=keyboards.kb_back)


@dp.message_handler(text='Back', state=Cards.editing_cards)
async def EditingCardsBack(message: types.message,
                           state: FSMContext):
    userdata = await state.get_data()
    await bot.send_message(chat_id=message.from_user.id,
                           text=userdata['deck_name'],
                           reply_markup=keyboards.kb_deckactions)
    await Cards.chosen.set()


@dp.message_handler(text='Back', state=Cards.removing_cards)
async def EditingCardsRemoveBack(message: types.Message,
                                 state: FSMContext):
    userdata = await state.get_data()
    await bot.send_message(chat_id=message.from_user.id,
                           text=userdata['deck_name'],
                           reply_markup=keyboards.kb_editing)
    await Cards.editing_cards.set()


# ----- Adding ----- #

@dp.message_handler(text='Add foreign', state=Cards.default)
async def CardsAdd(message: types.Message):
    await Cards.add.set()
    await bot.send_message(chat_id=message.from_user.id, text='Enter the ID', reply_markup=keyboards.kb_cancel)


# Ввод id добавляемой карточки
@dp.message_handler(state=Cards.add)
async def CardsAdded(message: types.Message, state: FSMContext):
    import json
    await state.update_data(id=message.text)
    await Cards.default.set()
    state_data = await state.get_data()

    # Проверяю, существует ли такая колода вообще
    with open('cards.json', 'r+') as file:
        data = json.load(file)
        decks_arr = [i for i in data]

        # если да - добавляю
        if any(state_data['id'] == i for i in decks_arr):
            with open('users.json', 'r+') as file:
                data = json.load(file)
                (data[f'{message.from_user.id}']).append(f"{state_data['id']}")
                file.seek(0)
                json.dump(data, file)
                await bot.send_message(chat_id=message.from_user.id, text='The deck is successfully added')
        else:
            await bot.send_message(chat_id=message.from_user.id, text="There's no deck with this ID")

    # если добавилась:
    await bot.send_message(chat_id=message.from_user.id, text="Here're your cards",
                           reply_markup=keyboards.kb_have_cards)


async def register_handlers(dp: Dispatcher):
    dp.register_message_handler(Start, commands='start', state='*')


# Setting up menu commands
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Start'),
    ]

    await bot.set_my_commands(commands)


async def main():
    # Configuring logging
    import logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    # Registering handlers
    await register_handlers(dp)

    # Setting up Commands: menu
    await set_commands(bot)

    # Starting polling
    await dp.start_polling()


asyncio.run(main())
