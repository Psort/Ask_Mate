import os
import time
from unicodedata import name
import database_common
from server import question_list
import bcrypt


QUESTION_HEADERS = ['id', 'submission_time', 'view_number',
                    'vote_number', 'title', 'message', 'image']
ANSWER_HEADERS = ['id', 'submission_time',
                  'vote_number', 'question_id', 'message', 'image']
SORT_QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number']


@database_common.connection_handler
def get_question_data(cursor):
    query = """
                SELECT question.*,users.username as user
                FROM question
                INNER JOIN users on users.id = question.user_id

            """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_questions_by_user_id(cursor,user_id):
    query = f"""
                SELECT *
                FROM question
                WHERE user_id = {user_id}
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_by_user_id(cursor,user_id):
    query = f"""
                SELECT *
                FROM answer
                WHERE user_id = {user_id}
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comments_by_user_id(cursor,user_id):
    query = f"""
                SELECT *
                FROM comment
                WHERE user_id = {user_id}
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comments(cursor):
    query = """
                SELECT comment.*,users.username as user
                FROM comment
                INNER JOIN users on users.id = comment.user_id
                ORDER BY comment.id
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_latest_question(cursor):
    query = """
            SELECT question.*,users.username as user
            FROM question
            INNER JOIN users on users.id = question.user_id
            ORDER BY submission_time DESC 
            LIMIT 5;
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_data(cursor):
    query = """
                SELECT answer.*,users.username as user
                FROM answer
                INNER JOIN users on users.id = answer.user_id
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_question_id(cursor, question_id):
    query = f"""
                SELECT comment.*,users.username as user
                FROM comment
                INNER JOIN users on users.id = comment.user_id
                WHERE comment.question_id = {question_id}
                ORDER BY comment.id
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    query = f"""
                SELECT question.*,users.username as user
                FROM question
                INNER JOIN users on users.id = question.user_id
                WHERE question.id = {question_id}
                ORDER BY question.id
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_by_id(cursor, answer_id):
    query = f"""
                SELECT answer.*,users.username as user
                FROM answer
                INNER JOIN users on users.id = answer.user_id
                WHERE answer.id= {answer_id}
                ORDER BY answer.id
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
                SELECT answer.*,users.username as user
                FROM answer
                INNER JOIN users on users.id = answer.user_id
                WHERE question_id = {question_id}
                ORDER BY answer.id
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
def get_all_tags(cursor):
    query = f"""
                SELECT *
                FROM question_tag
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
def get_question_by_tag_id(cursor, tag_id):
    query = f"""
                Select * FROM question
                WHERE id IN (SELECT question_id FROM question_tag WHERE tag_id = {tag_id})

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
                WHERE id = {question_id};
                SELECT user_id FROM question
                WHERE id = {question_id}
            """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def add_reputation(cursor, user_id, num_of_reputation):
    query = f"""
                UPDATE users
                SET reputation = reputation + {num_of_reputation}
                WHERE id = {user_id}
            """
    cursor.execute(query)


# @database_common.connection_handler
# def add_reputation_for_voteup(cursor, question_id, user_id, points):
#     query = f"""
#                 UPDATE users
#                 SET users.reputation = users.reputation + {points}
#                 INNER JOIN question
#                 ON question.user_id = users.id
#                 WHERE users.id = {user_id}
#             """
#     cursor.execute(query)


@database_common.connection_handler
def dislike_question(cursor, question_id):
    query = f"""
                UPDATE question
                SET dislike = dislike + 1 ,view_number = view_number - 1
                WHERE id = {question_id};
                SELECT user_id FROM question
                WHERE id = {question_id}
    """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def dislike_answer(cursor, answer_id):
    query = f"""
            UPDATE answer
            SET dislike = dislike + 1
            WHERE id = {answer_id};
            SELECT question_id, user_id FROM answer WHERE id = {answer_id}
            """
    cursor.execute(query)
    return cursor.fetchone()


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
                SELECT question_id, user_id FROM answer WHERE id = {answer_id}  
            """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def add_new_question(cursor, title, message, image,user_id):
    submission_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if image != 'NULL':
        image = f"'{image}'"
    query = f"""
                INSERT INTO question (user_id,submission_time, view_number, vote_number, title, message, image, dislike)
                VALUES ({user_id},'{submission_time}', -1, 0, '{title}', '{message}', {image}, 0) 
                RETURNING id
    """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def add_new_answer(cursor, question_id, message, image,user_id):
    submission_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if image != 'NULL':
        image = f"'{image}'"
    query = f"""
                INSERT INTO answer (user_id,submission_time, vote_number, question_id, message, image, dislike)
                VALUES ({user_id},'{submission_time}', 0, {question_id}, '{message}', {image}, 0) 
                RETURNING question_id
        """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def add_comment_to_question(cursor, question_id, message,user_id):
    submission_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    query = f"""
                    INSERT INTO comment (user_id,question_id, answer_id, message, submission_time, edited_count)
                    VALUES ('{user_id}',{question_id}, NULL, '{message}', '{submission_time}', 0) 
                    RETURNING question_id
            """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def add_comment_to_answer(cursor, answer_id, message,user_id):

    submission_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    query = f"""
                    INSERT INTO comment (user_id,question_id, answer_id, message, submission_time, edited_count)
                    VALUES ('{user_id}',NULL, {answer_id}, '{message}', '{submission_time}', 0) 

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
                SET message = '{message}', image = '{image}'
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
def del_tag(cursor, question_id):

    query = f"""
                DELETE FROM question_tag
                WHERE question_id = {question_id}
            """
    cursor.execute(query)

@database_common.connection_handler
def del_tag_from_question(cursor, question_id, tag_id):

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
                SELECT question.*,users.username as user
                FROM question
                INNER JOIN users on users.id = question.user_id 
                WHERE title LIKE '%{search_item}%'
                OR message LIKE '%{search_item}%'

            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def search_answers(cursor, search_item):
    query = f"""
            SELECT question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image,users.username as user
            FROM question
            INNER JOIN users on users.id = question.user_id 
            JOIN answer ON question.id = answer.question_id
            WHERE answer.message LIKE '%{search_item}%'
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_id(cursor, comment_id):
    query = f"""
                SELECT comment.*,users.username as user
                FROM comment
                INNER JOIN users on users.id = comment.user_id
                WHERE comment.id= {comment_id}
                ORDER BY comment.id
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


@database_common.connection_handler
def get_users(cursor):
    query = f"""
                SELECT * from users
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_user_by_user_id(cursor,user_id):
    query = f"""
                SELECT * from users
                WHERE id = '{user_id}'
            """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def create_account(cursor,username,password):
    registration_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"""
            INSERT INTO users (username,password,registration_date,num_asked_question,num_answer,num_comment,reputation)
            VALUES ('{username}', '{password}', '{registration_date}',0, 0, 0, 0);
        """
    cursor.execute(query)


@database_common.connection_handler
def get_users_list(cursor):
    query = f"""
        SELECT id, username, registration_date, num_asked_question, num_answer, num_comment, reputation
        FROM users
        ORDER BY id asc;
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_user_id_by_username(cursor,username):
    query = f"""
        SELECT id
        FROM users
        WHERE username = '{username}'
        ORDER BY id asc;
    """
    cursor.execute(query)
    return cursor.fetchone()



@database_common.connection_handler
def accepted_answer(cursor, question_id, answer_id):
    query = f"""
                UPDATE question
                SET accepted_answer = {answer_id}
                WHERE id = {question_id};
                SELECT user_id 
                FROM answer
                WHERE id = {answer_id}
        """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def reset_accepted_answer(cursor, question_id, answer_id):
    query = f"""
                UPDATE question
                SET accepted_answer = Null
                WHERE id = {question_id};
                SELECT user_id 
                FROM answer
                WHERE id = {answer_id}
        """
    cursor.execute(query)
    return cursor.fetchone()

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


def try_login(username,password):
    users = get_users()
    for user in users:
        if username == user['username']:
                return verify_password(password,user['password'])
    return False


@database_common.connection_handler
def get_tags_quantity_by_question(cursor):
    query = '''
            SELECT tag.id, tag.name , count (question_tag.question_id)
            FROM tag
            INNER JOIN question_tag
            ON tag.id = question_tag.tag_id
            GROUP BY tag.id
    '''
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_tags_quantity_by_question(cursor):
    query = '''
            SELECT tag.id, tag.name , count (question_tag.question_id)
            FROM tag
            INNER JOIN question_tag
            ON tag.id = question_tag.tag_id
            GROUP BY tag.id
    '''
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def count_question(cursor, user_id):
    query = f"""
        UPDATE users
        SET num_asked_question = num_asked_question + 1
        WHERE users.id = {user_id}
    """
    cursor.execute(query)

@database_common.connection_handler
def count_answers(cursor, user_id):
    query = f"""
        UPDATE users
        SET num_answer = users.num_answer + 1
        WHERE users.id = {user_id}
    """
    cursor.execute(query)

@database_common.connection_handler
def count_comments(cursor, user_id):
    query = f"""
        UPDATE users
        SET num_comment = users.num_comment + 1
        WHERE users.id = {user_id}
    """
    cursor.execute(query)

def check_is_username(username):
    users = get_users()
    for user in users:
        if username == user['username']:
            return False
    return True


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)
