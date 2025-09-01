import os


quiz = {}
quiz_list = []

path = 'quiz-questions'
for dirs, folder, files in os.walk(path):
    for file in files:
        with open(f'{dirs}/{file}', 'r', encoding='KOI8-R') as my_file:
            questions = my_file.read()
            splitted_questions = questions.split('\n\n\n')
            for question in splitted_questions:
                splitted_question = question.split('\n\n')
                quiz_list.append(splitted_question)
                for i, el in enumerate(splitted_question):
                    if 'Вопрос' in el:
                        question = el.replace('\n', ' ').strip()
                        quiz[question] = ''
                    elif 'Ответ' in el:
                        quiz[question] = el.replace('\n', ' ')[6:-1].strip()
