import sqlite3

con = sqlite3.connect("server.db")

cur = con.cursor()

for value in cur.execute("SELECT * FROM entrance_test_b2c"):
    q = value[1]
    ans_1 = value[2]
    ans_2 = value[3]
    ans_3 = value[4]
    answers = [ans_1, ans_2, ans_3]
    print(q, answers)

# c_id = get_chat_id(update, context)
# q = 'What is the capital of Italy?'
# answers = ['Rome', 'London', 'Amsterdam']
# message = context.bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=0)
