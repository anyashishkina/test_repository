import telebot
from telebot import types
from telebot.types import BotCommand
import sqlite3

bot = telebot.TeleBot('5844570225:AAHVbCClhE53DdtM-RpZ1vKjrPPB4j_I538', 'markdown')
con = sqlite3.connect("server.db", check_same_thread=False)
cur = con.cursor()
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()


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
                   description='Выбрать тест b2c')]

    bot.set_my_commands(main_menu_commands)


def db_table_val(user_id: int, user_name: str, user_status: str, username: str):
    cursor.execute('INSERT INTO users (user_id, user_name, user_status, username) VALUES (?, ?, ?, ?)',
                   (user_id, user_name, user_status, username))
    conn.commit()

def db_table_statistics(id: int, user_name: str, first_name: str, test_password: int, correct_answers: int, boss_id: str):
    cur.execute('INSERT INTO statistics (id, user_name, first_name, test_password, correct_answers) VALUES (?, ?, ?, ?, ?)',
                (id, user_name, first_name, test_password, correct_answers))
    con.commit()


test_id = 2
b2b_or_b2c = 0
test = 0
question_number = 1
correct_option = -1
result = 0
level = 0
id_for_statistics = 1
current_user = ''


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
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
                if test_id == 29:
                    bot.send_message(message.from_user.id, 'Входной тест завершён.',
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
        elif b2b_or_b2c == 0:
            for value in cur.execute("SELECT * FROM entrance_test_b2c WHERE id=?", (test_id,)):
                answers = [value[2], value[3], value[4]]
                correct_option = value[5]
                bot.send_poll(chat_id=message.chat.id, question=value[1], options=answers, type='quiz',
                              correct_option_id=value[5], open_period=30, is_anonymous=False)
                test_id += 1
                if test_id == 25:
                    bot.send_message(message.from_user.id, 'Входной тест завершён.',
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
    else:
        bot.send_message(message.from_user.id, "Я вас не понимаю. Напишите /help.")


@bot.poll_answer_handler()
def handle_poll_answer(poll_answer):
    global result, correct_option, test_id, b2b_or_b2c, test, level, current_user
    selected_option = poll_answer.option_ids[0]
    if correct_option == selected_option:
        result += 1
    if test_id == 25 and b2b_or_b2c == 0:
        b2b_or_b2c = 2
        bot.send_message(poll_answer.user.id, f'Вы набрали {result} баллов из 25')
        if result <= 25 and result >= 23:
            test += 300
            level += 300
            bot.send_message(poll_answer.user.id,
                             'На данный момент ваш уровень - эксперт. Вам будут предложены тесты из этой категории')
        elif result <= 22 and result >= 20:
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
    elif test_id == 29 and b2b_or_b2c == 1:
        b2b_or_b2c = 2
        bot.send_message(poll_answer.user.id, f'Вы набрали {result} баллов из 29')
        if result <= 25 and result >= 23:
            test += 300
            level += 300
            bot.send_message(poll_answer.user.id,
                             'На данный момент ваш уровень - эксперт. Вам будут предложены тесты из этой категории')
        elif result <= 22 and result >= 20:
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
        cur.execute(
            'UPDATE statistics SET correct_answers = ? WHERE user_name = ?',
            (result, current_user))
        con.commit()
        b2b_or_b2c = 2
        bot.send_message(poll_answer.user.id, f'Вы ответили верно на {result} из 3 вопросов')
        result = 0


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global b2b_or_b2c, test, question_number, correct_option, test_id, id_for_statistics, current_user
    if call.data == "manager" or "boss":
        if call.data == "manager":
            user_name = call.from_user.username
            first_name = call.from_user.first_name
            cur.execute(
                'INSERT INTO statistics (id, user_name, first_name) VALUES (?, ?, ?)',
                (id_for_statistics, user_name, first_name))
            con.commit()
            id_for_statistics += 1
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
            db_table_val(user_id=us_id, user_name=us_name, user_status=status, username=username)
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
        sms5 = 'Поздравляю! Вы готовы проходить тест. Он будет сгенеривован нашей системой.'
        bot.send_message(call.message.chat.id, sms5)
    if test in [2121, 2122, 2123, 2111, 2112, 2113, 2131, 2132, 2133, 2141, 2142, 2143]:
        current_user = call.from_user.username
        cur.execute(
            'UPDATE statistics SET test_password = ? WHERE user_name = ?',
            (test, current_user))

        con.commit()
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


global current_state
current_state = []
key_word = {}


@bot.message_handler()
def ask_key_word(message):
    msg = message.text
    msg = "'" + msg + "'"
    info_msg = cursor.execute("SELECT * FROM testbase WHERE test_id =" + str(msg)).fetchall()
    user_to = message.from_user.id
    key_word[user_to] = []
    key_word[user_to].append(msg)
    key_word[user_to].append(info_msg)
    while len(info_msg) > 0:
        current_state.append('receiving')
        send = bot.send_message(message.chat.id, 'Такой  пароль для доступа уже существует, придумайте новый')
        bot.register_next_step_handler(send, make_key_word)
        while (current_state[-1] != 'answering'):
            current_state_str = 'receiving'
            if current_state[-1] == 'answering':
                break
        info_msg = key_word[user_to][1]
    send = bot.send_message(message.chat.id, 'Ваш пароль успешно добавлен. Введите количество вопросов')
    bot.register_next_step_handler(send, numbers)


def make_key_word(message):
    msg = message.text
    user_to = message.from_user.id
    msg = "'" + msg + "'"
    info_msg = cursor.execute("SELECT * FROM testbase WHERE test_id = " + str(msg)).fetchall()
    if len(info_msg) == 0:
        key_word[user_to][0] = msg
    key_word[user_to].append(info_msg)
    current_state.append('answering')


@bot.message_handler()
def numbers(message):
    global i
    global j
    i = 0
    amount = message.text.split()[0]
    while (amount.isdigit() == False):
        current_state.append('receiving')
        send = bot.send_message(message.chat.id, 'Введите число, а не текст')
        bot.register_next_step_handler(send, read_number)
        while (current_state[-1] != 'answering'):
            current_state_str = 'receiving'
            if current_state[-1] == 'answering':
                break
        amount = current_state[-2]
    while (i != int(amount)):
        current_state.append('receiving')
        send = bot.send_message(message.chat.id, f'Введите {i + 1}-й вопрос')
        bot.register_next_step_handler(send, questions)
        while (current_state[-1] != 'answering'):
            current_state_str = 'receiving'
            if current_state[-1] == 'answering':
                break
        j = 0
        while (j != 4):
            current_state.append('receiving')
            send = bot.send_message(message.chat.id, f'Введите {j + 1}-й вариант ответа')
            bot.register_next_step_handler(send, answers)
            while (current_state[-1] != 'answering'):
                current_state_str = 'receiving'
                if current_state[-1] == 'answering':
                    break
            j += 1
        current_state.append('receiving')
        send = bot.send_message(message.chat.id, f'Введите номер правильного ответа')
        bot.register_next_step_handler(send, answers)
        while (current_state[-1] != 'answering'):
            current_state_str = 'receiving'
            if current_state[-1] == 'answering':
                break
        i += 1
    current_state.clear()


def read_number(message):
    amount = message.text
    if amount.isdigit() == True:
        current_state.append(amount)
    current_state.append('answering')


def questions(message):
    last = message.text
    user_to = message.from_user.id
    user_to = key_word[user_to][0]
    user_to = int(user_to[1:-1])
    add_question(i + 1, last, user_to)
    current_state.append('answering')


def answers(message):
    ans = message.text
    user_to = message.from_user.id
    user_to = key_word[user_to][0]
    user_to = int(user_to[1:-1])
    add_ans(ans, user_to, i + 1, j + 1)
    current_state.append('answering')


def add_test(question_number, question, ans_1, ans_2, ans_3, ans_4, right_ans, test_id):
    cursor.execute(
        'INSERT INTO testbase (question_number, question, ans_1 ,ans_2 ,ans_3,ans_4, right_ans, test_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (question_number, question, ans_1, ans_2, ans_3, ans_4, right_ans, test_id))
    conn.commit()


def add_question(question_number, question, test_id):
    cursor.execute(
        'INSERT INTO testbase (question_number,question, test_id) VALUES (?,?, ?)',
        (question_number, question, test_id))
    conn.commit()


def add_ans(ans, test_id, question_number, j_t):
    if (j_t != 5):
        answer = 'ans_'
        answer += str(j_t)
    else:
        answer = 'right_ans'
    string = 'UPDATE testbase SET ' + answer + '= ? WHERE test_id=? and question_number=?'
    cursor.execute(
        string,
        (ans, test_id, question_number))
    conn.commit()


if __name__ == '__main__':
    set_main_menu()
    bot.polling(none_stop=True, interval=0)
