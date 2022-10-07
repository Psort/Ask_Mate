import data_manager
import bcrypt

def check_is_username(username):
    users = data_manager.get_users()
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



def is_tag_in_tags(tag):
    tags = data_manager.get_tags()
    for element in tags:
        if tag == element["name"]:
            return False
    return True


def check_tag_in_question(question_id, tag):
    question_tags = data_manager.get_tags_by_question_id(question_id)
    for question_tag in question_tags:
        if tag == question_tag['name']:
            return False
    return True


def try_login(username,password):
    users = data_manager.get_users()
    for user in users:
        if username == user['username']:
                return verify_password(password,user['password'])
    return False

def get_info_user(user_id):
    user = data_manager.get_user_by_user_id(user_id)
    questions = data_manager.get_questions_by_user_id(user_id)
    answers = data_manager.get_answers_by_user_id(user_id)
    comments = data_manager.get_comments_by_user_id(user_id)
    tags = data_manager.get_tags()
    profile_tag = data_manager.get_all_tags()
    return user,questions,answers,comments,tags,profile_tag


def get_info_to_main_webside():
    user_posts = data_manager.get_latest_question()
    user_answers = data_manager.get_answer_data()
    comments = data_manager.get_comments()
    tags = data_manager.get_tags()
    profile_tag = data_manager.get_all_tags()
    return user_posts,user_answers,comments,tags,profile_tag


def get_current_user_info(user_id):
    user = data_manager.get_user_by_user_id(user_id)
    questions = data_manager.get_questions_by_user_id(user_id)
    answers = data_manager.get_answers_by_user_id(user_id)
    comments = data_manager.get_comments_by_user_id(user_id)
    tags = data_manager.get_tags()
    profile_tag = data_manager.get_all_tags()
    notifications = data_manager.get_notifications_by_user_id(user_id)
    return user,questions,answers,comments,tags,profile_tag,notifications

def get_info_to_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    comments = data_manager.get_comments()
    question_tags = data_manager.get_tags_by_question_id(question_id)
    return question,answers,comments,question_tags