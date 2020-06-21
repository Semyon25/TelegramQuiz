import xml.etree.ElementTree as etree


# получить вопрос (параметр - номер вопроса: 1, 2, ...)
def get_question(question_number):
    tree = etree.parse('quiz.xml')
    items = tree.getroot().find('items')
    question_text = items[question_number-1].find('question').text
    answers_text = []
    answers = items[question_number-1].find('answers').findall('answer')
    for answer in answers:
        answers_text.append(answer.find('text').text)
    return [question_text, answers_text]


# Возвращает результат теста
def get_result_quiz(total_balls):
    tree = etree.parse('quiz.xml')
    results = tree.getroot().find('results')
    for result in results:
        if int(result.find('min').text) <= total_balls <= int(result.find('max').text):
            return [result.find('title').text, result.find('description').text]
    return ['Error', '']


# Возвращает количество баллов за ответ на определенный вопрос
def get_balls_for_question(question_number, answer_id):
    tree = etree.parse('quiz.xml')
    items = tree.getroot().find('items')
    point = items[question_number-1].find('answers').findall('answer')[answer_id].find('point').text
    return int(point)


# Общий балл за все отвеченные вопросы
def get_balls_for_all_questions(answers):
    total = 0
    for answer in answers:
        question_number = int(answer.replace('q',''))
        answer_number = int(answers[answer])
        total += get_balls_for_question(question_number, answer_number)
    return total


# Суммарное количество вопросов
def total_questions():
    tree = etree.parse('quiz.xml')
    items = tree.getroot().find('items')
    return len(items)