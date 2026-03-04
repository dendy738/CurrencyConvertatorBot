from time import sleep
import requests
import telebot
from datetime import datetime
import user_requests_history

# 8491831536:AAE0MmhH5U4RU-wV426PcpfxNRAG9QYqJCs - token for my bot
my_bot = telebot.TeleBot('8491831536:AAE0MmhH5U4RU-wV426PcpfxNRAG9QYqJCs')
chat_id = None
users = {}

# Bot Greeting!
@my_bot.message_handler(func=lambda message: message.text in ('Hello', 'Hi'))
def get_chat_id(message):
    global chat_id
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('/start', '/help')
    my_bot.send_message(message.chat.id, 'Hi!\nChoose some command: /start or /help', reply_markup=keyboard)


# Depending on option ('start' or 'help') creating new keyboard

@my_bot.message_handler(commands=['start', 'help'])
def greeting(message):
    if message.text == '/start':
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Currency Convert', 'Currency exchange rate info')
        my_bot.send_message(message.chat.id, 'Choose what option you want: ', reply_markup=keyboard)
    elif message.text == '/help':
        my_bot.send_message(message.chat.id, 'Bot was created special for get to know what is the current currency exchange rate!')
        sleep(0.5)
        my_bot.send_message(message.chat.id, 'After command /start you will choose either currency convert or currency exchange rate info! Remember, you always can return to start step by writing /start or /help!')
        sleep(0.5)
        my_bot.send_message(message.chat.id, '''"Currency Convert" is responsible for conversation from your currency to currency you want.\n"Currency exchange rate info" is responsible for currency exchange rate info you want.''')


# Step 1: User choose currency conversation or exchange rate info and will create keyboard buttons with currencies

@my_bot.message_handler(func= lambda message: message.text in ('Currency Convert', 'Currency exchange rate info'))
def if_button_currency_convert(message):
    if message.text == 'Currency Convert':
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('EUR', 'USD')
        keyboard.row('PLN', 'GBP')
        keyboard.row('UAH')
        my_bot.send_message(message.chat.id, 'Choose currency that you have ', reply_markup=keyboard)
    elif message.text == 'Currency exchange rate info':
        keyboard = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton('EUR', callback_data='eur')
        btn2 = telebot.types.InlineKeyboardButton('USD', callback_data='usd')
        btn3 = telebot.types.InlineKeyboardButton('PLN', callback_data='pln')
        btn4 = telebot.types.InlineKeyboardButton('GBP', callback_data='gbp')
        keyboard.add(btn1, btn2, btn3, btn4)
        my_bot.send_message(message.chat.id, 'Choose currency which information you want to get', reply_markup=keyboard)


# Here we are sending get-request for getting info of each currency
try:
    bot_request = requests.get('https://api.monobank.ua/bank/currency').json()
    eur = None
    usd = None
    pln = None
    gbp = None

    for cur in bot_request:
        if cur['currencyCodeA'] == 978 and cur['currencyCodeB'] == 980:
            eur = cur
        elif cur['currencyCodeA'] == 840 and cur['currencyCodeB'] == 980:
            usd = cur
        elif cur['currencyCodeA'] == 985 and cur['currencyCodeB'] == 980:
            pln = cur
        elif cur['currencyCodeA'] == 826 and cur['currencyCodeB'] == 980:
            gbp = cur
        else:
            continue
except Exception as e:
    print('You must waiting 5 seconds before trying again')

# Step 2: If user chose currency conversation next step will set user choice

user_choice = None

@my_bot.message_handler(func=lambda message: message.text in ('EUR', 'USD', 'PLN', 'GBP', 'UAH'))
def set_choice_of_user(message):
    global user_choice
    if message.text == 'EUR':
        my_bot.send_message(message.chat.id, 'Enter your balance')
        user_choice = message.text
    elif message.text == 'USD':
        my_bot.send_message(message.chat.id, 'Enter your balance')
        user_choice = message.text
    elif message.text == 'PLN':
        my_bot.send_message(message.chat.id, 'Enter your balance')
        user_choice = message.text
    elif message.text == 'GBP':
        my_bot.send_message(message.chat.id, 'Enter your balance')
        user_choice = message.text
    elif message.text == 'UAH':
        my_bot.send_message(message.chat.id, 'Enter your balance')
        user_choice = message.text


# Step 3: At this step we are setting a user balance and choice of currency that in which user want to convert

user_balance = None

@my_bot.message_handler(func=lambda message: message.text.isnumeric())
def set_balance_of_user(message):
    global user_balance
    user_balance = float(message.text)
    keyboard = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(text='EUR', callback_data='EUR')
    btn2 = telebot.types.InlineKeyboardButton(text='USD', callback_data='USD')
    btn3 = telebot.types.InlineKeyboardButton(text='PLN', callback_data='PLN')
    btn4 = telebot.types.InlineKeyboardButton(text='GBP', callback_data='GBP')
    btn5 = telebot.types.InlineKeyboardButton(text='UAH', callback_data='UAH')
    keyboard.add(btn1, btn2, btn3, btn4, btn5)
    my_bot.send_message(message.chat.id, 'Choose what currency you want to convert', reply_markup=keyboard)

# Step 4: User get result of request to conversation


qty_convert_requests = 0
user_convert_requests = {}
@my_bot.callback_query_handler(func=lambda call: call.data in ('EUR', 'USD', 'PLN', 'GBP', 'UAH'))
def currency_convert_process(call):
    global user_balance, user_choice, qty_convert_requests, user_convert_requests, users

    if call.data == 'EUR':
        match user_choice:
            case 'EUR':
                my_bot.send_message(call.message.chat.id, f'{user_balance:.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'USD':
                usd_to_eur = usd.get('rateBuy') / eur.get('rateBuy')
                my_bot.send_message(call.message.chat.id, f'{(user_balance * usd_to_eur):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'PLN':
                pln_to_eur = pln.get('rateCross') / eur.get('rateBuy')
                my_bot.send_message(call.message.chat.id, f'{(user_balance * pln_to_eur):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'GBP':
                gbp_to_eur = gbp.get('rateCross') / eur.get('rateBuy')
                my_bot.send_message(call.message.chat.id, f'{(user_balance * gbp_to_eur):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'UAH':
                my_bot.send_message(call.message.chat.id, f'{(user_balance / eur.get('rateBuy')):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)

    elif call.data == 'USD':
        match user_choice:
            case 'EUR':
                eur_to_usd = eur.get('rateBuy') / usd.get('rateBuy')
                my_bot.send_message(call.message.chat.id, f'{(user_balance * eur_to_usd):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'USD':
                my_bot.send_message(call.message.chat.id, f'{user_balance:.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'PLN':
                pln_to_usd = pln.get('rateCross') / usd.get('rateBuy')
                my_bot.send_message(call.message.chat.id, f'{(user_balance * pln_to_usd):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'GBP':
                gbp_to_usd = gbp.get('rateCross') / usd.get('rateBuy')
                my_bot.send_message(call.message.chat.id, f'{(user_balance * gbp_to_usd):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'UAH':
                my_bot.send_message(call.message.chat.id, f'{(user_balance / usd.get('rateBuy')):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)

    elif call.data == 'PLN':
        match user_choice:
            case 'EUR':
                eur_to_pln = eur.get('rateBuy') / pln.get('rateCross')
                my_bot.send_message(call.message.chat.id, f'{(user_balance * eur_to_pln):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'USD':
                usd_to_pln = usd.get('rateBuy') / pln.get('rateCross')
                my_bot.send_message(call.message.chat.id, f'{(user_balance * usd_to_pln):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'PLN':
                my_bot.send_message(call.message.chat.id, f'{user_balance:.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'GBP':
                gbp_to_pln = gbp.get('rateCross') / pln.get('rateCross')
                my_bot.send_message(call.message.chat.id, f'{(user_balance * gbp_to_pln):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'UAH':
                my_bot.send_message(call.message.chat.id, f'{(user_balance / pln.get('rateCross')):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)

    elif call.data == 'GBP':
        match user_choice:
            case 'EUR':
                eur_to_gbp = eur.get('rateBuy') / gbp.get('rateCross')
                my_bot.send_message(call.message.chat.id, f'{(user_balance * eur_to_gbp):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'USD':
                usd_to_gbp = usd.get('rateBuy') / gbp.get('rateCross')
                my_bot.send_message(call.message.chat.id, f'{(user_balance * usd_to_gbp):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'PLN':
                pln_to_gbp = pln.get('rateCross') / gbp.get('rateCross')
                my_bot.send_message(call.message.chat.id, f'{(user_balance * pln_to_gbp):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'GBP':
                my_bot.send_message(call.message.chat.id, f'{user_balance:.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'UAH':
                my_bot.send_message(call.message.chat.id, f'{(user_balance / gbp.get('rateCross')):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)

    elif call.data == 'UAH':
        match user_choice:
            case 'EUR':
                my_bot.send_message(call.message.chat.id, f'{(user_balance * eur.get('rateBuy')):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'USD':
                my_bot.send_message(call.message.chat.id, f'{(user_balance * usd.get('rateBuy')):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'PLN':
                my_bot.send_message(call.message.chat.id, f'{(user_balance * pln.get('rateCross')):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'GBP':
                my_bot.send_message(call.message.chat.id, f'{(user_balance * gbp.get('rateCross')):.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)
            case 'UAH':
                my_bot.send_message(call.message.chat.id, f'{user_balance:.2f} {call.data}')
                qty_convert_requests += 1
                forward_message_time = call.message.date
                normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
                user_convert_requests[qty_convert_requests] = (user_choice, call.data, normal_time)

    if len(user_convert_requests) == 10:
        user_requests_history.write_conversation_to_file(user_convert_requests)
        qty_convert_requests = 0
        user_convert_requests = {}


users_currency_info_req = {}
qty_info_requests = 0
@my_bot.callback_query_handler(func=lambda call: call.data in ('eur', 'usd', 'pln', 'gbp'))
def currency_info(call):
    global users_currency_info_req, qty_info_requests, users
    if call.data == 'eur':
        my_bot.send_message(call.message.chat.id, f'Currency: EUR, You sell: {eur.get('rateBuy'):.2f}, You buy: {eur.get('rateSell'):.2f}')
        forward_message_time = call.message.date
        normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
        qty_info_requests += 1
        users_currency_info_req[qty_info_requests] = (call.data, normal_time)
    elif call.data == 'usd':
        my_bot.send_message(call.message.chat.id, f'Currency: USD, You sell: {usd.get('rateBuy'):.2f}, You buy: {usd.get('rateSell'):.2f}' )
        forward_message_time = call.message.date
        normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
        qty_info_requests += 1
        users_currency_info_req[qty_info_requests] = (call.data, normal_time)
    elif call.data == 'pln':
        my_bot.send_message(call.message.chat.id, f'Currency: PLN, You sell: {pln.get('rateCross'):.2f}, You buy: No info')
        forward_message_time = call.message.date
        normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
        qty_info_requests += 1
        users_currency_info_req[qty_info_requests] = (call.data, normal_time)
    elif call.data == 'gbp':
        my_bot.send_message(call.message.chat.id, f'Currency: GBP, You sell: {gbp.get('rateCross'):.2f}, You buy: No info')
        forward_message_time = call.message.date
        normal_time = datetime.fromtimestamp(forward_message_time).strftime('%H:%M:%S')
        qty_info_requests += 1
        users_currency_info_req[qty_info_requests] = (call.data, normal_time)

    if len(users_currency_info_req) == 10:
        user_requests_history.write_get_info_to_file(users_currency_info_req)
        qty_info_requests = 0
        users_currency_info_req = {}


my_bot.infinity_polling()