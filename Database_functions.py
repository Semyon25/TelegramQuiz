from time import ctime
import sqlite3
from sqlite3 import Error
import pandas as pd
from dict2xml import dict2xml
import xmltodict

DATABASE_NAME = 'quiz.db'
TABLE_NAME = 'USERS'


# COLUMNS = {'user_id', 'username', 'first_name', 'last_name', 'reg_date', 'answers', 'summa'}


# отправка запроса
def post_sql_query(sql_query):
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
        except Error:
            pass
        result = cursor.fetchall()
        return result


# Создание таблицы
def create_tables():
    users_query = f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} 
                        (user_id INTEGER PRIMARY KEY NOT NULL,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        reg_date TEXT,
                        answers TEXT,
                        summa TEXT);'''
    post_sql_query(users_query)


# регистрация нового пользователя
def register_user(user_id, username, first_name, last_name):
    user_check_query = f'SELECT * FROM {TABLE_NAME} WHERE user_id = {user_id};'
    user_check_data = post_sql_query(user_check_query)
    if not user_check_data:
        insert_to_db_query = f'INSERT INTO {TABLE_NAME} (user_id, username, first_name,  last_name, reg_date) VALUES ({user_id}, "{username}", "{first_name}", "{last_name}", "{ctime()}");'
        post_sql_query(insert_to_db_query)


# получение таблицы
def read_all_data_in_table():
    with sqlite3.connect(DATABASE_NAME) as connection:
        df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", connection)
        return df


# обновление ячейки в таблице
def update_cell(user_id, name_column, value):
    query = f"UPDATE {TABLE_NAME} SET {name_column} = '{value}' WHERE user_id = {user_id};"
    post_sql_query(query)


# получение значения ячейки
def read_cell(user_id, name_column):
    query = f'SELECT {name_column} FROM {TABLE_NAME} WHERE user_id = {user_id};'
    answer = post_sql_query(query)
    return answer[0][0]


def xml_to_dict(xml_str):
    try:
        my_dict = xmltodict.parse(xml_str)['answers']
    except:
        my_dict = []
    return dict(my_dict)


def dict_to_xml(my_dict):
    data_str = dict2xml(my_dict, 'answers')
    return data_str


# добавление ответа
def set_answer(user_id, question_number, answer_number):
    ans_str = read_cell(user_id, 'answers')
    ans_dict = xml_to_dict(ans_str)
    ans_dict[f'q{question_number}'] = answer_number
    ans_str = dict_to_xml(ans_dict)
    update_cell(user_id, 'answers', ans_str)


# возвращает номер вопроса, на который еще нет ответа
def first_not_answered_question(user_id):
    answers_str = read_cell(user_id, 'answers')
    answers_dict = xml_to_dict(answers_str)
    counter = 1
    while True:
        if f'q{counter}' not in answers_dict.keys():
            return counter
        else:
            counter += 1


# получение словаря с ответами пользователя
def get_answers_dict(user_id):
    ans_str = read_cell(user_id, 'answers')
    ans_dict = xml_to_dict(ans_str)
    return ans_dict
