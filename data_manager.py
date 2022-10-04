import os
import time
from unicodedata import name
import database_common
from server import question_list

users = {'john@doe.com': 'a'}

QUESTION_HEADERS = ['id', 'submission_time', 'view_number',
                    'vote_number', 'title', 'message', 'image']
ANSWER_HEADERS = ['id', 'submission_time',
                  'vote_number', 'question_id', 'message', 'image']
SORT_QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number']


@database_common.connection_handler
def get_question_data(cursor):
    query = """
                SELECT *
                FROM question
                ORDER BY id
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def  get_comments(cursor):
    query = """
                SELECT *
                FROM comment
                ORDER BY id
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_latest_question(cursor):
    query = """
            SELECT * 
            FROM question
            ORDER BY submission_time DESC 
            LIMIT 5;
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_data(cursor):
    query = """
                SELECT *
                FROM answer
                ORDER BY id
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_question_id(cursor, question_id):
    query = f"""
                SELECT *
                FROM comment
                WHERE question_id = {question_id}
                ORDER BY id
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    query = f"""
                SELECT *
                FROM question
                WHERE id = {question_id}
                ORDER BY id
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_by_id(cursor, answer_id):
    query = f"""
                SELECT *
                FROM answer
                WHERE id= {answer_id}
                ORDER BY id
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_view(cursor, question_id):
    query = f"""
                UPDATE question
                SET view_number = view_number + 1
                WHERE id = {question_id}
            """
    cursor.execute(query)


@database_common.connection_handler
def get_answers_by_question_id(cursor, question_id):
    query = f"""
                SELECT *
                FROM answer
                WHERE question_id = {question_id}
                ORDER BY id
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_tags(cursor):
    query = f"""
                SELECT *
                FROM tag
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_tags_by_question_id(cursor, question_id):
    query = f"""
                Select * FROM tag
                WHERE id IN (SELECT tag_id FROM question_tag WHERE question_id = {question_id})

            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    query = f"""
                SELECT question_id
                FROM answer
                WHERE id = {answer_id}
            """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def add_like_question(cursor, question_id):
    query = f"""
                UPDATE question
                SET vote_number = vote_number + 1 ,view_number = view_number - 1
                WHERE id = {question_id}
            """
    cursor.execute(query)


@database_common.connection_handler
def dislike_question(cursor, question_id):
    query = f"""
                UPDATE question
                SET dislike = dislike + 1 ,view_number = view_number - 1
                WHERE id = {question_id}
    """
    cursor.execute(query)


@database_common.connection_handler
def add_like_answer(cursor, id):
    query = f"""
            UPDATE answer
            SET vote_number = vote_number + 1
            WHERE id = {id}
            """
    cursor.execute(query)


@database_common.connection_handler
def dislike_answer(cursor, answer_id):
    query = f"""
            UPDATE answer
            SET dislike = dislike + 1 ,view_number = view_number - 1
            WHERE id = {answer_id}
            """
    cursor.execute(query)


@database_common.connection_handler
def delte_vote(cursor, id):
    query = f"""
            UPDATE question
            SET view_number = view_number - 1
            WHERE id = {id}"""
    cursor.execute(query)


@database_common.connection_handler
def add_like_answer(cursor, answer_id):
    query = f"""
                UPDATE answer
                SET vote_number = vote_number + 1
                WHERE id = {answer_id};
                SELECT question_id FROM answer WHERE id = {answer_id}
--                 RETURNING question_id
            """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def add_new_question(cursor, title, message, image):
    submission_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if image != 'NULL':
        image = f"'{image}'"
    query = f"""
                INSERT INTO question (submission_time, view_number, vote_number, title, message, image, dislike)
                VALUES ('{submission_time}', -1, 0, '{title}', '{message}', {image}, 0) 
                RETURNING id
    """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def add_new_answer(cursor, question_id, message, image):
    submission_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if image != 'NULL':
        image = f"'{image}'"
    query = f"""
                INSERT INTO answer (submission_time, vote_number, question_id, message, image, dislike)
                VALUES ('{submission_time}', 0, {question_id}, '{message}', {image}, 0) 
                RETURNING question_id
        """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def add_comment_to_question(cursor, question_id, message):
    submission_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    query = f"""
                    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
                    VALUES ({question_id}, NULL, '{message}', '{submission_time}', 0) 
                    RETURNING question_id
            """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def add_comment_to_answer(cursor, answer_id, message):
    submission_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    query = f"""
                    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
                    VALUES (NULL, {answer_id}, '{message}', '{submission_time}', 0) 

            """
    cursor.execute(query)


@database_common.connection_handler
def edit_question(cursor, question_id, title, message, image):
    if image != 'NULL':
        image = f"'{image}'"
    query = f"""
                UPDATE question
                SET title = '{title}', message = '{message}', image = {image},view_number = view_number - 1
                WHERE id = {question_id}
    """
    cursor.execute(query)


@database_common.connection_handler
def edit_answer(cursor, answer_id, message, image):
    if image != 'NULL':
        image = f"'{image}'"
    query = f"""
                UPDATE answer
                SET message = "{message}", image = {image}
                WHERE id = {answer_id}
                RETURNING question_id
        """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def del_question(cursor, question_id):
    del_tag(question_id)
    del_comment(question_id)
    del_answer(False, question_id)

    query = f"""
                DELETE FROM question
                WHERE id = {question_id}
            """
    cursor.execute(query)


@database_common.connection_handler
def del_answer(cursor, answer_id=False, question_id=False):

    if type(question_id) == int:
        del_comment_by_question_id(question_id)

        a_id = f'question_id = {question_id}'

    if type(answer_id) == int:
        del_comment(False, answer_id)
        a_id = f'id = {answer_id}'

    query = f"""
                DELETE FROM answer
                WHERE {a_id}
                RETURNING question_id
            """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def del_comment(cursor, question_id=False, answer_id=False, comment_id=False):

    if type(comment_id) == int:
        q_id = f'id = {comment_id}'

    if type(answer_id) == int:
        q_id = f'answer_id = {answer_id}'

    if type(question_id) == int:
        q_id = f'question_id = {question_id}'

    query = f"""
                DELETE FROM comment
                WHERE {q_id}
                RETURNING question_id
            """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def del_tag(cursor, question_id, tag_id):

    query = f"""
                DELETE FROM question_tag
                WHERE question_id = {question_id} AND tag_id = {tag_id}
            """
    cursor.execute(query)


@database_common.connection_handler
def del_comment_by_question_id(cursor, question_id):

    query = f"""
                DELETE FROM comment
                WHERE answer_id IN (SELECT id FROM answer WHERE question_id = {question_id})
            """
    cursor.execute(query)


@database_common.connection_handler
def search_question(cursor, search_item):

    query = f"""
                SELECT *
                FROM question 
                WHERE title LIKE '%{search_item}%'
                OR message LIKE '%{search_item}%'

            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def search_answers(cursor, search_item):
    query = f"""
            SELECT question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image 
            FROM question
            JOIN answer ON question.id = answer.question_id
            WHERE answer.message LIKE '%{search_item}%'
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_id(cursor, comment_id):
    query = f"""
                SELECT *
                FROM comment
                WHERE id= {comment_id}
                ORDER BY id
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def edit_comment(cursor, comment_id, message):
    submission_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"""
                UPDATE comment
                SET message = '{message}', edited_count = edited_count + 1, submission_time = '{submission_time}'
                WHERE id = {comment_id}
                RETURNING id
        """
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def add_tag(cursor, tag):
    query = f""" 
            INSERT into tag (name) VALUES('{tag}');
            """
    cursor.execute(query)

@database_common.connection_handler
def add_tag_to_question(cursor, question_id, tag):
    if is_tag_in_tags(tag):
        add_tag(tag)
    if check_tag_in_question(question_id, tag):
        query = f""" 
                    INSERT into question_tag (question_id,tag_id)
                    VALUES({question_id},(SELECT id from tag WHERE name = '{tag}')) 
            """
        cursor.execute(query)

@database_common.connection_handler
def delete_view(cursor,question_id):
    query = f"""
                UPDATE question
                SET view_number = view_number - 1
                WHERE id = {question_id}
            """
    cursor.execute(query)


def is_tag_in_tags(tag):
    tags = get_tags()
    for element in tags:
        if tag == element["name"]:
            return False
    return True


def check_tag_in_question(question_id, tag):
    question_tags = get_tags_by_question_id(question_id)
    for question_tag in question_tags:
        if tag == question_tag['name']:
            return False
    return True

def check_is_username(username,password):
    if username in users:
        if password == users[username]:
            return True
    return False
