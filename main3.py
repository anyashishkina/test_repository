import flask
import telebot
from telebot import types
from telebot.types import BotCommand 
import sqlite3
import json
from flask import Flask, render_template


bot = telebot.TeleBot('5844570225:AAHVbCClhE53DdtM-RpZ1vKjrPPB4j_I538', 'markdown')
con = sqlite3.connect("server.db", check_same_thread=False)
cur = con.cursor()
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
app = Flask(__name__)



def set_main_menu():
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Запуск бота'),
        BotCommand(command='/help',
                   description='Помощь'),
        BotCommand(command='/addtest',
                   description='Добавить тест'),
        BotCommand(command='/choosetestb2b',
                   description='Выбрать тест b2b'),
        BotCommand(command='/choosetestb2c',
                   description='Выбрать тест b2c'),
        BotCommand(command='/show_statistic',
                   description='Просмотр статистики')
    ]

    bot.set_my_commands(main_menu_commands)


def db_table_val(user_id: int, user_name: str, user_surname: str, user_status: str, boss_id: int, test_password: int, correct_answers: int):
    cur.execute('INSERT INTO users_for_statistics(user_id, user_name, user_surname, user_status, boss_id, test_password, correct_answers ) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (user_id, user_name, user_surname, user_status, boss_id, test_password, correct_answers))
    con.commit()


def db_table_val1(user_id: int, user_name: str, user_status: str, username: str):
    cursor.execute('INSERT INTO users (user_id, user_name, user_status, username) VALUES (?, ?, ?, ?)',
                   (user_id, user_name, user_status, username))
    conn.commit()


def db_table_val2(user_id: int, user_status: str, user_boss: str):
    cursor.execute('INSERT INTO boss_to_users (user_id, user_status, user_boss) VALUES (?, ?, ?)',
                   (user_id, user_status, user_boss))
    conn.commit()


# results = {
#     "test1": 0, "test2": 1, "test3": 0,
#     "test4": 2, "test5": 3, "test6": 1,
#     "test7": 0, "test8": 3, "test9": 1,
#     "test10": 2, "test11": 3, "test12": 1,
# }
#
# with app.app_context():
#     def posts():
#         matrix = [list(results.values())[i:i + 4] for i in range(0, len(results), 4)]
#         return render_template('statistics.html', matrix=matrix)


test_id = 2
b2b_or_b2c = 0
test = 0
question_number = 1
correct_option = -1
result = 0
level = 0


@bot.message_handler(content_types=['text'])
def get_text_messages(message, massege=None):
    global test_id, b2b_or_b2c, test_id, question_number, correct_option, test, result, level
    sms2 = 'Вы можете выбрать один из 4 типов клиентов: '
    if message.text == "/start":
        test_id = 2
        b2b_or_b2c = 0
        test = 0
        question_number = 1
        correct_option = -1
        result = 0
        keyboard = types.InlineKeyboardMarkup()
        key_manager = types.InlineKeyboardButton(text='Менеджер', callback_data="manager")
        keyboard.add(key_manager)
        key_boss = types.InlineKeyboardButton(text='Управляющий', callback_data="boss")
        keyboard.add(key_boss)
        bot.send_message(message.from_user.id, 'Выберите вашу роль', reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напишите /start")
    elif message.text == "/show_statistic":
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # matrix = [list(results.values())[i:i + 4] for i in range(0, len(results), 4)]
        webAppTest=types.WebAppInfo(f"statistics.html?matrix=1")
        murkup.add(types.InlineKeyboardButton('Посмотреть статистику', web_app=webAppTest))
    elif message.text == "Привет":
        bot.send_message(message.from_user.id, "Здравствуйте! Напишите /help")
    elif message.text.lower() == 'добавить тест' or message.text.lower() == '/addtest':
        send = bot.send_message(message.chat.id,
                                'Создайте пароль для доступа к вашему тесту, он может состоять только цифр')
        bot.register_next_step_handler(send, ask_key_word)
    elif message.text == '/choosetestb2b':
        if str(test)[0] == "2":
            bot.send_message(message.chat.id,
                             'Вы проходили входной тест для B2C, поэтому можете выбрать тест только из этой категории. Нажмите "Выбрать тест b2c"')
        else:
            test = 1000
            test += level
            question_number = 1
            keyboard = types.InlineKeyboardMarkup()
            key_loyal = types.InlineKeyboardButton(text='Лояльный', callback_data='loyal_client')
            key_new = types.InlineKeyboardButton(text='Новый', callback_data='new_client')
            key_negative = types.InlineKeyboardButton(text='Негативный', callback_data='negative_client')
            key_doubting = types.InlineKeyboardButton(text='Сомневающийся', callback_data='doubting_client')
            keyboard.add(key_loyal)
            keyboard.add(key_new)
            keyboard.add(key_negative)
            keyboard.add(key_doubting)
            bot.send_message(message.from_user.id, 'Выберите тип клиента', reply_markup=keyboard)
    elif message.text == '/choosetestb2c':
        if str(test)[0] == "1":
            bot.send_message(message.chat.id,
                             'Вы проходили входной тест для B2B, поэтому можете выбрать тест только из этой категории. Нажмите "Выбрать тест b2b"')
        else:
            test = 2000
            test += level
            question_number = 1
            keyboard = types.InlineKeyboardMarkup()
            key_loyal = types.InlineKeyboardButton(text='Лояльный', callback_data='loyal_client')
            key_new = types.InlineKeyboardButton(text='Новый', callback_data='new_client')
            key_negative = types.InlineKeyboardButton(text='Негативный', callback_data='negative_client')
            key_doubting = types.InlineKeyboardButton(text='Сомневающийся', callback_data='doubting_client')
            keyboard.add(key_loyal)
            keyboard.add(key_new)
            keyboard.add(key_negative)
            keyboard.add(key_doubting)
            bot.send_message(message.from_user.id, 'Выберите тип клиента', reply_markup=keyboard)
    elif message.text == "Следующий вопрос":
        if b2b_or_b2c == 1:
            for value in cur.execute("SELECT * FROM entrance_test_b2b WHERE id=?", (test_id,)):
                answers = [value[2], value[3], value[4]]
                correct_option = value[5]
                bot.send_poll(chat_id=message.chat.id, question=value[1], options=answers, type='quiz',
                              correct_option_id=value[5], open_period=30, is_anonymous=False)
                test_id += 1
                if test_id == 4:
                    # if test_id == 29:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    button_next_question = types.KeyboardButton('Выбрать тест')
                    markup.row(button_next_question)
                    bot.send_message(message.from_user.id, 'Нажмите кнопку "Выбрать тест", когда будете готовы.',
                                     reply_markup=markup)
        elif b2b_or_b2c == 0:
            for value in cur.execute("SELECT * FROM entrance_test_b2c WHERE id=?", (test_id,)):
                answers = [value[2], value[3], value[4]]
                correct_option = value[5]
                bot.send_poll(chat_id=message.chat.id, question=value[1], options=answers, type='quiz',
                              correct_option_id=value[5], open_period=30, is_anonymous=False)
                test_id += 1
                if test_id == 4:
                    # if test_id == 25:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    button_next_question = types.KeyboardButton('Выбрать тест')
                    markup.row(button_next_question)
                    bot.send_message(message.from_user.id, 'Нажмите кнопку "Выбрать тест", когда будете готовы.',
                                     reply_markup=markup)
        else:
            for value in cur.execute("SELECT * FROM main_tests WHERE test_password=? AND question_number=?",
                                     (test, question_number,)):
                answers = [value[3], value[4], value[5]]
                correct_option = value[6]
                bot.send_poll(chat_id=message.chat.id, question=value[2], options=answers, type='quiz',
                              correct_option_id=value[6], open_period=30, is_anonymous=False)
                question_number += 1
            if question_number == 4:
                bot.send_message(message.from_user.id, 'Тест завершён.',
                                 reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Выбрать тест':
        bot.send_message(message.chat.id, "Вам предстоит выбрать тип клиента и форму коммуникаций",
                         reply_markup=types.ReplyKeyboardRemove())
        keyboard = types.InlineKeyboardMarkup()
        key_loyal = types.InlineKeyboardButton(text='Лояльный', callback_data='loyal_client')
        key_new = types.InlineKeyboardButton(text='Новый', callback_data='new_client')
        key_negative = types.InlineKeyboardButton(text='Негативный', callback_data='negative_client')
        key_doubting = types.InlineKeyboardButton(text='Сомневающийся', callback_data='doubting_client')
        keyboard.add(key_loyal)
        keyboard.add(key_new)
        keyboard.add(key_negative)
        keyboard.add(key_doubting)
        bot.send_message(message.chat.id, sms2, reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, "Я вас не понимаю. Напишите /help.")


@bot.poll_answer_handler()
def handle_poll_answer(poll_answer):
    global result, correct_option, test_id, test, b2b_or_b2c, level
    selected_option = poll_answer.option_ids[0]
    if correct_option == selected_option:
        result += 1
    if test_id == 4 and b2b_or_b2c == 0:
        # if test_id == 25 and b2b_or_b2c == 0:
        b2b_or_b2c = 2
        bot.send_message(poll_answer.user.id, f'Вы набрали {result} баллов из 25')

        if 25 >= result >= 23:
            test += 300
            level += 300
            bot.send_message(poll_answer.user.id,
                             'На данный момент ваш уровень - эксперт. Вам будут предложены тесты из этой категории')
        elif 22 >= result >= 20:
            test += 200
            level += 200
            bot.send_message(poll_answer.user.id,
                             'На данный момент ваш уровень - продвинутый. Вам будут предложены тесты из этой категории')
        elif result <= 19:
            test += 100
            level += 100
            bot.send_message(poll_answer.user.id,
                             'На данный момент ваш уровень - новичок. Вам будут предложены тесты из этой категории')
        result = 0
    elif test_id == 4 and b2b_or_b2c == 1:
        # elif test_id == 29 and b2b_or_b2c == 1:
        b2b_or_b2c = 2
        bot.send_message(poll_answer.user.id, f'Вы набрали {result} баллов из 29')
        if 25 >= result >= 23:
            test += 300
            level += 300
            bot.send_message(poll_answer.user.id,
                             'На данный момент ваш уровень - эксперт. Вам будут предложены тесты из этой категории')
        elif 22 >= result >= 20:
            test += 200
            level += 200
            bot.send_message(poll_answer.user.id,
                             'На данный момент ваш уровень - продвинутый. Вам будут предложены тесты из этой категории')
        elif result <= 19:
            test += 100
            level += 100
            bot.send_message(poll_answer.user.id,
                             'На данный момент ваш уровень - новичок. Вам будут предложены тесты из этой категории')
        result = 0
    elif question_number == 4 and b2b_or_b2c == 2:
        cur.execute('UPDATE users_for_statistics SET correct_answers=? WHERE test_password=?', (result, test))
        con.commit()
        b2b_or_b2c = 2
        bot.send_message(poll_answer.user.id, f'Вы набрали {result} баллов из 3')
        result = 0



@bot.message_handler(content_types=['web_app_data'])
def web_app(message: types.Message):
    res = json.loads(message.web_app_data.data)
    first_name = res.get("subordinate-first-name")
    last_name = res.get("subordinate-last-name")
    if first_name is not None and last_name is not None:
        bot.send_message(message.from_user.id, f'Имя: {first_name}\nФамилия: {last_name}',
                         reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.from_user.id, "Данные отсутствуют", reply_markup=types.ReplyKeyboardRemove())


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global b2b_or_b2c, test, question_number, correct_option, test_id
    if call.data == "manager" or "boss":
        if call.data == "manager":
            bot.send_message(call.from_user.id, "Вам предстоит выбрать тип продаж. ")
            b2b_msg = "B2B (Business to Business) – модель, когда клиенты компании – это другие фирмы или предприниматели."
            bot.send_message(call.from_user.id, b2b_msg)
            keyboard = types.InlineKeyboardMarkup()
            key_b2b = types.InlineKeyboardButton(text='B2B', callback_data="typeofclientb")
            keyboard.add(key_b2b)
            key_b2c = types.InlineKeyboardButton(text='B2C', callback_data="typeofclientc")
            keyboard.add(key_b2c)
            b2c_msg = "B2C(Business to Consumer) предполагает продажу товаров,услуг физическим лицам/конечным потребителям."
            bot.send_message(call.from_user.id, b2c_msg, reply_markup=keyboard)
        elif call.data == "boss":
            db_table_val(user_id=call.from_user.id, user_name=call.from_user.first_name,
                         user_surname=call.from_user.last_name, user_status='manager', boss_id=0, test_password=0, correct_answers=0)

            bot.send_message(call.message.chat.id, 'Вы можете создать свой тест')
        user_to = call.from_user.id
        info_user_to = cursor.execute("SELECT * FROM users WHERE user_id = " + str(user_to)).fetchall()
        if len(info_user_to) > 0:
            pass
        else:
            us_id = call.from_user.id
            us_name = call.from_user.first_name
            if call.data == "manager":
                status = "manager"
            else:
                status = "boss"
            username = call.from_user.username
            db_table_val1(user_id=us_id, user_name=us_name, user_status=status, username=username)
            if status == 'manager':
                db_table_val2(user_id=us_id, user_status=status, user_boss=0)
                send = bot.send_message(call.message.chat.id, 'Введите id вашего руководителя')
                bot.register_next_step_handler(send, set_boss)

    if call.data == "typeofclientb" or call.data == "typeofclientc":
        if call.data == "typeofclientb" or call.data == "typeofclientc":
            if call.data == "typeofclientb":
                test += 1000
                b2b_or_b2c = 1
                sms1 = 'Отлично! Вы выбрали продажи компании/магазину. Пожалуйста пройдите тест для определения уровня.'
                bot.send_message(call.message.chat.id, sms1)
                for value in cur.execute("SELECT * FROM entrance_test_b2b"):
                    answers = [value[2], value[3], value[4]]
                    correct_option = value[5]
                    bot.send_poll(chat_id=call.message.chat.id, question=value[1], options=answers, type='quiz',
                                  correct_option_id=value[5], open_period=30, is_anonymous=False)
                    test_id += 1
                    break
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_next_question = types.KeyboardButton('Следующий вопрос')
                markup.row(button_next_question)
                bot.send_message(call.message.chat.id,
                                 'Когда будете готовы перейти к следующему вопросу, нажмите кнопку "Следующий вопрос" ',
                                 reply_markup=markup)
            else:
                test += 2000
                sms1 = 'Отлично! Вы выбрали продажи частному лицу. Пожалуйста пройдите тест для определения уровня.'
                bot.send_message(call.message.chat.id, sms1)
                for value in cur.execute("SELECT * FROM entrance_test_b2c"):
                    answers = [value[2], value[3], value[4]]
                    correct_option = value[5]
                    bot.send_poll(chat_id=call.message.chat.id, question=value[1], options=answers, type='quiz',
                                  correct_option_id=value[5], open_period=30, is_anonymous=False)
                    test_id += 1
                    break
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_next_question = types.KeyboardButton('Следующий вопрос')
                markup.row(button_next_question)
                bot.send_message(call.message.chat.id,
                                 'Когда будете готовы перейти к следующему вопросу, нажмите кнопку "Следующий вопрос" ',
                                 reply_markup=markup)
    elif call.data == 'loyal_client' or call.data == 'new_client' or call.data == 'negative_client' or call.data == 'doubting_client':
        if call.data == 'loyal_client':
            test += 10
        elif call.data == 'new_client':
            test += 20
        elif call.data == 'negative_client':
            test += 30
        elif call.data == 'doubting_client':
            test += 40
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
            test += 1
        elif call.data == 'meet_communication':
            test += 2
        elif call.data == 'message_communication':
            test += 3

        sms5 = 'Поздравляю! Вы готовы проходить тест. Он будет сгенерирован нашей системой.'
        bot.send_message(call.message.chat.id, sms5)
        cnt = 0
        for value in cur.execute("SELECT * FROM users_for_statistics"):
            if call.from_user.id == value[0] and test == value[5]:
                cnt += 1
        if cnt == 0:
            db_table_val(user_id=call.from_user.id, user_name=call.from_user.first_name,
                         user_surname=call.from_user.last_name, user_status='manager', boss_id=0, test_password=test,
                         correct_answers=0)
    if test in [2121, 2122, 2123, 2111, 2112, 2113, 2131, 2132, 2133, 2141, 2142, 2143]:
        for value in cur.execute("SELECT * FROM main_tests WHERE test_password=? AND question_number=?",
                                 (test, question_number,)):
            answers = [value[3], value[4], value[5]]
            correct_option = value[6]
            bot.send_poll(chat_id=call.message.chat.id, question=value[2], options=answers, type='quiz',
                          correct_option_id=value[6], open_period=30, is_anonymous=False)
            question_number += 1
            break
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_next_question = types.KeyboardButton('Следующий вопрос')
        markup.row(button_next_question)
        bot.send_message(call.message.chat.id,
                         'Когда будете готовы перейти к следующему вопросу, нажмите кнопку "Следующий вопрос" ',
                         reply_markup=markup)


def set_boss(message):
    msg = message.text
    user_id = message.from_user.id
    string = 'UPDATE boss_to_users SET user_boss = ? WHERE user_id=? '
    cursor.execute(
        string,
        (msg, user_id))
    conn.commit()


from collections import defaultdict

user_id_to_keywords = defaultdict(list)
test_id_to_numbers = defaultdict(list)
test_id_to_ans = defaultdict(list)
states = defaultdict(list)
user_to_keywords = defaultdict(list)


@bot.message_handler()
def ask_key_word(message):
    keyword = message.text
    user_id = message.from_user.id
    user_to_keywords[user_id] = keyword
    keyword_list = cursor.execute(f"SELECT * FROM testbase WHERE test_id ='{keyword}'").fetchall()
    if len(keyword_list) > 0:
        msg = bot.send_message(message.chat.id, 'Такой  пароль для доступа уже существует, придумайте новый')
        bot.register_next_step_handler(msg, ask_key_word)
    else:
        user_id = message.from_user.id
        user_id_to_keywords[user_id].append(keyword)
        msg = bot.send_message(message.chat.id, 'Ваш пароль успешно добавлен.')
        cursor.execute(
            'INSERT INTO testbase (question_number,test_id) VALUES (?, ?)',
            (1, keyword))
        conn.commit()
        msg = bot.send_message(message.chat.id, 'Введите количество вопросов')
        bot.register_next_step_handler(msg, numbers)


@bot.message_handler()
def numbers(message):
    amount = message.text.split()[0]
    user_id = message.from_user.id
    keyword = user_id_to_keywords[user_id][-1]
    while (amount.isdigit() == False):
        send = bot.send_message(message.chat.id, 'Введите число, а не текст')
        bot.register_next_step_handler(send, numbers)
    test_id_to_numbers[keyword].append(amount)
    send = bot.send_message(message.chat.id, 'Введите 1-й вопрос')
    bot.register_next_step_handler(send, read_questions)


def read_questions(message):
    msg = message.text
    user_id = message.from_user.id
    keyword = user_id_to_keywords[user_id][-1]
    amount = int(test_id_to_numbers[keyword][0])
    if len(test_id_to_numbers[keyword]) == 1:
        test_id_to_numbers[keyword].append(1)
    elif len(test_id_to_numbers[keyword]) == 2:
        test_id_to_numbers[keyword].append(2)
        string = 'INSERT INTO testbase (question_number,test_id) VALUES(?,?)'
        cursor.execute(
            string,
            (2, keyword))
        conn.commit()
    elif len(test_id_to_numbers[keyword]) > 2:
        quest_num = int(test_id_to_numbers[keyword][-1]) + 1
        test_id_to_numbers[keyword].append(quest_num)
        string = 'INSERT INTO testbase (question_number,test_id) VALUES(?,?)'
        cursor.execute(
            string,
            (quest_num, keyword))
        conn.commit()
    string = 'UPDATE testbase SET question = ? WHERE test_id=? and question_number=?'
    cursor.execute(
        string,
        (msg, keyword, int(test_id_to_numbers[keyword][-1])))
    conn.commit()
    send = bot.send_message(message.chat.id, f'Введите 1-й вариант ответа')
    bot.register_next_step_handler(send, read_ans)
    states[keyword].append('receiving')
    while (states[keyword][-1] != 'answering'):
        if states[keyword][-1] == 'answering':
            break
    if int(test_id_to_numbers[keyword][-1]) + 1 <= int(test_id_to_numbers[keyword][0]):
        send = bot.send_message(message.chat.id, f'Введите {int(test_id_to_numbers[keyword][-1]) + 1}-й вопрос')
        bot.register_next_step_handler(send, read_questions)


def read_ans(message):
    cnt = 0
    msg = message.text
    amount = msg.split()[0]
    user_id = message.from_user.id
    keyword = user_id_to_keywords[user_id][-1]
    if len(test_id_to_ans[keyword]) != 0:
        if test_id_to_ans[keyword][-1] == 5:
            if amount.isdigit() == False:
                cnt = 1
                msg = bot.send_message(message.chat.id, 'Введите число, а не текст')
                bot.register_next_step_handler(msg, read_ans)
    if cnt == 0:
        if len(test_id_to_ans[keyword]) == 0:
            test_id_to_ans[keyword].append(2)
        else:
            test_id_to_ans[keyword].append(test_id_to_ans[keyword][-1] + 1)
        if test_id_to_ans[keyword][-1] == 6:
            answer = 'right_ans'
        elif test_id_to_ans[keyword][-1] < 6:
            answer = 'ans_' + str(test_id_to_ans[keyword][-1] - 1)
        if len(test_id_to_ans[keyword]) <= 5:
            string = 'UPDATE testbase SET ' + answer + ' = ? WHERE test_id=? and question_number=?'
            cursor.execute(
                string,
                (msg, keyword, int(test_id_to_numbers[keyword][-1])))
            conn.commit()
        if test_id_to_ans[keyword][-1] < 5:
            send = bot.send_message(message.chat.id, f'Введите {int(test_id_to_ans[keyword][-1])}-й вариант ответа')
            bot.register_next_step_handler(send, read_ans)
        if test_id_to_ans[keyword][-1] == 5:
            send = bot.send_message(message.chat.id, f'Введите номер правильного варианта ответа')
            bot.register_next_step_handler(send, read_ans)
        if test_id_to_ans[keyword][-1] == 6:
            test_id_to_ans[keyword].clear()
            states[keyword].append('answering')


if __name__ == '__main__':
    set_main_menu()
    bot.polling(none_stop=True, interval=0)


# matrix_str = json.dumps(matrix)
# response = requests.post("https://anyashishkina.github.io/test_repository/", data={'matrix': matrix_str})
# response_data = response.json()
# webAppTest = types.WebAppInfo(response_data)
# for value in cursor.execute("SELECT * FROM users WHERE user_id=?", (message.chat.id,)):
#     if value[2] == 'boss':
#         murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         murkup.add(types.InlineKeyboardButton('Посмотреть статистику', web_app=webAppTest))
#     else:
#         murkup = types.InlineKeyboardMarkup()
#         murkup.add(types.InlineKeyboardButton('Посмотреть статистику', web_app=webAppTest))
# bot.send_message(message.chat.id, 'Статистика!', reply_markup=murkup)
# response = requests.post("https://anyashishkina.github.io/test_repository/", data={'matrix': matrix_str})
# murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
# with open("statistics.html") as file:
#     template = file.read()
#     webAppTest = template.format(message=matrix)
#     murkup.add(types.InlineKeyboardButton('Посмотреть статистику', web_app=webAppTest))
#     bot.send_message(message.chat.id, 'Статистика!', reply_markup=murkup)



