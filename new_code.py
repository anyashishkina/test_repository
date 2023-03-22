import telebot
from telebot import types
import sqlite3

con = sqlite3.connect("server.db", check_same_thread=False)
cur = con.cursor()

bot = telebot.TeleBot('5844570225:AAHVbCClhE53DdtM-RpZ1vKjrPPB4j_I538')

global conclusion
conclusion = []

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Здравствуйте!<крутое приветствие>")
        bot.send_message(message.from_user.id, "Вам предстоит выбрать тип продаж. ")
        b2b_msg = "B2B (Business to Business) – модель, когда клиенты компании – это другие фирмы или предприниматели."
        bot.send_message(message.from_user.id, b2b_msg)

        keyboard = types.InlineKeyboardMarkup()
        key_b2b = types.InlineKeyboardButton(text='B2B', callback_data='typeofclientb')
        keyboard.add(key_b2b)
        key_b2c = types.InlineKeyboardButton(text='B2C', callback_data='typeofclientc')
        keyboard.add(key_b2c)
        b2c_msg = "B2C(Business to Consumer) предполагает продажу товаров,услуг физическим лицам/конечным потребителям."
        bot.send_message(message.from_user.id, b2c_msg, reply_markup=keyboard)

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напишите /start")
    elif message.text == "Привет":
        bot.send_message(message.from_user.id, "Здравствуйте! Напишите /help")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

# def f(call, message):
#     if call.data == "typeofclientb" or call.data == "typeofclientc":
#         if call.data == "typeofclientb":
            

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "typeofclientb" or call.data == "typeofclientc":
        sms2 = 'Вы можете выбрать один из 4 вариантов: '
        if call.data == "typeofclientb":
            sms1 = 'Отлично! Вы выбрали продажи компании/магазину.Теперь нужно выбрать тип клиента'
            conclusion.append('b2b')
            markup = types.ReplyKeyboardMarkup()
            button_next_question = types.KeyboardButton('Следующий вопрос', callback_data='next_question')
            markup.row(button_next_question)
            bot.send_message(call.message.chat.id, reply_markup=markup)
            for value in cur.execute("SELECT * FROM entrance_test_b2b"):
                q = value[1]
                ans_1 = value[2]
                ans_2 = value[3]
                ans_3 = value[4]
                answers = [ans_1, ans_2, ans_3]
                bot.send_poll(chat_id=call.message.chat.id, question=value[1], options=answers, type='quiz',
                              correct_option_id=value[5], explanation='мы молодцы', open_period=10)
                if call.data == 'next_question':
                    bot.send_poll(chat_id= call.message.chat.id, question=q, options=answers, type='quiz', correct_option_id=value[5], explanation='мы молодцы', open_period=10)
        else:
            sms1 = 'Отлично! Вы выбрали продажи частному лицу. Теперь нужно выбрать тип клиента'
            conclusion.append('b2c')
            for value in cur.execute("SELECT * FROM entrance_test_b2c"):
                q = value[1]
                ans_1 = value[2]
                ans_2 = value[3]
                ans_3 = value[4]
                answers = [ans_1, ans_2, ans_3]
                bot.send_poll(chat_id= call.message.chat.id, question= q, options=answers, type='quiz', correct_option_id=value[5], explanation='мы молодцы', open_period=10)
        keyboard = types.InlineKeyboardMarkup()
        key_loyal = types.InlineKeyboardButton(text='Лояльный', callback_data='loyal_client')
        key_new = types.InlineKeyboardButton(text='Новый', callback_data='new_client')
        key_negative = types.InlineKeyboardButton(text='Негативный', callback_data='negative_client')
        key_doubting = types.InlineKeyboardButton(text='Сомневающийся', callback_data='doubting_client')
        bot.send_message(call.message.chat.id, sms1)
        keyboard.add(key_loyal)
        keyboard.add(key_new)
        keyboard.add(key_negative)
        keyboard.add(key_doubting)
        bot.send_message(call.message.chat.id, sms2, reply_markup=keyboard)
        bot.send_message(call.message.chat.id, 'It works!', reply_markup=markup)
    elif call.data == 'loyal_client' or call.data == 'new_client' or call.data == 'negative_client' or call.data == 'doubting_client':
        if call.data == 'loyal_client':
            conclusion.append('loyal')
        elif call.data == 'new_client':
            conclusion.append('new')
        elif call.data == 'negative_client':
            conclusion.append('negative')
        elif call.data == 'doubting_client':
            conclusion.append('doubting')
        sms3 = 'Давайте выберем форму коммуникации'
        keyboard = types.InlineKeyboardMarkup()
        key_phone = types.InlineKeyboardButton(text='Телефон', callback_data='phone_communication')
        key_meet = types.InlineKeyboardButton(text='Личная встреча', callback_data='meet_communication')
        key_message = types.InlineKeyboardButton(text='Переписка', callback_data='message_communication')
        keyboard.add(key_phone)
        keyboard.add(key_meet)
        keyboard.add(key_message)
        bot.send_message(call.message.chat.id, sms3, reply_markup=keyboard)
    elif call.data == 'phone_communication' or call.data == 'meet_communication' or call.data == 'message_communication':
        if call.data == 'phone_communication':
            conclusion.append('phone')
        elif call.data == 'meet_communication':
            conclusion.append('meet')
        elif call.data == 'message_communication':
            conclusion.append('message')
        sms4 = 'Осталось выбрать уровень'
        keyboard = types.InlineKeyboardMarkup()
        key_level1 = types.InlineKeyboardButton(text='Новичок', callback_data='level1')
        key_level2 = types.InlineKeyboardButton(text='Продвинутый', callback_data='level2')
        key_level3 = types.InlineKeyboardButton(text='Эксперт', callback_data='level3')
        keyboard.add(key_level1)
        keyboard.add(key_level2)
        keyboard.add(key_level3)
        bot.send_message(call.message.chat.id, sms4, reply_markup=keyboard)
    elif call.data == 'level1' or call.data == 'level2' or call.data == 'level3':
        sms5 = 'Поздравляю! Вы готовы проходить тест. Он будет сгенеривован нашей системой.'
        bot.send_message(call.message.chat.id, sms5)

bot.polling(none_stop=True, interval=0)
