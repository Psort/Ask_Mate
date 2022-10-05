from multiprocessing.connection import answer_challenge
from operator import itemgetter
from flask import Flask, render_template, request, redirect, url_for, session
import data_manager
import connection
import bcrypt

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'


# @app.route('/')
# def display_latest_questions():
#     pass


@app.route('/')
def route_list():
    user_posts = data_manager.get_latest_question()
    user_answers = data_manager.get_answer_data()
    comments = data_manager.get_comments()
    tags = data_manager.get_tags()
    profile_tag = data_manager.get_all_tags()
    return render_template('list.html', headers=data_manager.SORT_QUESTION_HEADERS, posts=user_posts,
                           answers=user_answers, list_button=1, comments=comments, session=session,tags=tags,profile_tag=profile_tag)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = "this acount dont exist"
    if session != {}:
        return redirect(url_for('profile'))
    else:
        if request.method == 'POST':
            session.pop('user_id', None)

            username = request.form['username']
            password = request.form['password']

            if data_manager.try_login(username, password):
                session['username'] = username
                session['id'] = data_manager.get_user_id_by_username(username)[
                    'id']
                return redirect(url_for('route_list'))
            return render_template('login.html', error_message=error_message)
        return render_template('login.html')


@app.route("/profile")
def profile():
    if session == {}:
        return redirect(url_for('login'))
    user = data_manager.get_user_by_user_id(session['id'])
    questions = data_manager.get_questions_by_user_id(session['id'])
    answers = data_manager.get_answers_by_user_id(session['id'])
    comments = data_manager.get_comments_by_user_id(session['id'])
    tags = data_manager.get_tags()
    profile_tag = data_manager.get_all_tags()
    return render_template('profile.html', user=user, questions=questions, answers=answers, comments=comments,
                           tags=tags, profile_tag=profile_tag)


@app.route('/Sign_up', methods=['GET', 'POST'])
def Sign_up():
    error_message = "such an account already exists"
    if session != {}:
        return redirect(url_for('profile'))
    else:
        if request.method == 'POST':
            session.pop('user_id', None)

            username = request.form['username']
            password = request.form['password']
            if data_manager.check_is_username(username):
                data_manager.create_account(username, password)
                session['username'] = username
                session['id'] = data_manager.get_user_id_by_username(username)[
                    'id']
                return redirect(url_for('profile'))
            return render_template('Sign_up.html', error_message=error_message)
        return render_template('Sign_up.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/list")
def question_list():
    order_by = request.args.get('order_by', 'submission_time')
    order_direction = request.args.get('order_direction', 'asc')
    questions = data_manager.get_question_data()
    comments = data_manager.get_comments()
    tags = data_manager.get_tags()
    profile_tag = data_manager.get_all_tags()
    sorted_questions = sorted(questions, key=itemgetter(
        order_by), reverse=order_direction == 'desc')

    return render_template('list.html', posts=sorted_questions, headers=data_manager.SORT_QUESTION_HEADERS,
                           comments=comments)


@app.route('/tags/<int:tag_id>')
def questions_by_tag_name(tag_id):
    question = data_manager.get_question_by_tag_id(tag_id)
    tag_id = request.form.get("id")

    return render_template('questions_by_tag.html', tag_id=tag_id, question=question)


@app.route('/question/<int:question_id>')
def display_question(question_id):
    data_manager.add_view(question_id)
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    comments = data_manager.get_comments()
    question_tags = data_manager.get_tags_by_question_id(question_id)

    return render_template('question.html', question_id=question_id, answers=answers, question=question,
                           question_tags=question_tags, comments=comments)


@app.route('/question/<int:question_id>/add_tag', methods=['POST'])
def add_tag(question_id):
    data_manager.delete_view(question_id)
    data_manager.add_view(question_id)
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    comments = data_manager.get_comment_by_question_id(question_id)
    question_tags = data_manager.get_tags_by_question_id(question_id)
    all_tags = data_manager.get_tags()
    return render_template('question.html', question_id=question_id, answers=answers, question=question,
                           question_tags=question_tags, all_tags=all_tags, comments=comments)


@app.route('/question/<int:question_id>/add_tag_to_question', methods=['POST'])
def add_tag_to_question(question_id):
    data_manager.delete_view(question_id)
    tag = request.form.get("tag")
    data_manager.add_tag_to_question(question_id, tag)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/question/<int:question_id>/add_vote', methods=['POST'])
def add_vote_question(question_id):
    if session == {}:
        return redirect(url_for('login'))
    data_manager.add_like_question(question_id)
    return redirect(url_for("display_question", question_id=question_id))


@app.route('/question/<int:question_id>/dislike', methods=['POST'])
def add_dislike_question(question_id):
    if session == {}:
        return redirect(url_for('login'))
    data_manager.dislike_question(question_id)
    return redirect(url_for("display_question", question_id=question_id))


@app.route('/answer/<int:answer_id>/add_vote', methods=['POST'])
def add_vote_answer(answer_id):
    if session == {}:
        return redirect(url_for('login'))
    question_id = data_manager.add_like_answer(answer_id)
    data_manager.delte_vote(question_id['question_id'])
    return redirect(url_for("display_question", question_id=question_id['question_id'], answer_id=answer_id))


@app.route('/answer/<int:answer_id>/add_dislike', methods=['POST'])
def add_dislike_answer(answer_id):
    if session == {}:
        return redirect(url_for('login'))
    question_id = data_manager.add_like_answer(answer_id)
    data_manager.dislike_answer(question_id['question_id'])
    return redirect(url_for("display_question", question_id=question_id['question_id'], answer_id=answer_id))


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if session == {}:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('add_question.html', question=None)
    elif request.method == 'POST':
        fileitem = request.files["filename"]
        filename = connection.add_file(fileitem)
        title = request.form['title']
        message = request.form['message']
        question_id = data_manager.add_new_question(title, message, filename, session['id'])
        return redirect(url_for('display_question', question_id=question_id['id']))


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if session == {}:
        return redirect(url_for('login'))
    if request.method == 'GET':
        question = data_manager.get_question_by_id(question_id)
        return render_template('add_question.html', question=question[0], question_id=question_id)
    elif request.method == 'POST':
        fileitem = request.files["filename"]
        filename = connection.add_file(fileitem)
        title = request.form['title']
        message = request.form['message']
        data_manager.edit_question(question_id, title, message, filename)
        return redirect(url_for('display_question', question_id=question_id))


@app.route('/add_answer/<int:question_id>', methods=['GET', 'POST'])
def add_answer(question_id):
    if session == {}:
        return redirect(url_for('login'))
    if request.method == 'GET':
        question = data_manager.get_question_by_id(question_id)
        return render_template('add_answer.html', post=question[0], answer=None)
    elif request.method == 'POST':
        data_manager.delete_view(question_id)
        fileitem = request.files["filename"]
        filename = connection.add_file(fileitem)
        message = request.form['message']
        question_id = data_manager.add_new_answer(question_id, message, filename, session['id'])
        return redirect(url_for('display_question', question_id=question_id['question_id']))


@app.route('/question/<int:question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if session == {}:
        return redirect(url_for('login'))
    if request.method == 'GET':
        user_posts = data_manager.get_question_data()
        return render_template('list.html', headers=data_manager.SORT_QUESTION_HEADERS, posts=user_posts,
                               question_id=question_id)
    elif request.method == 'POST':
        message = request.form['message']
        data_manager.add_comment_to_question(question_id, message, user_id=session['id'])
        return redirect(url_for('route_list'))


@app.route('/answer/<int:answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    if session == {}:
        return redirect(url_for('login'))
    if request.method == 'GET':
        question_id = data_manager.get_question_id_by_answer_id(answer_id)
        question = data_manager.get_question_by_id(question_id['question_id'])
        answers = data_manager.get_answers_by_id(answer_id)
        comments = data_manager.get_comments()
        return render_template('question.html', answer_id=answer_id, answers=answers, question=question,
                               comments=comments, question_id=question_id['question_id'])
    elif request.method == 'POST':
        message = request.form['message']
        data_manager.add_comment_to_answer(answer_id, message, session['id'])
        question_id = data_manager.get_question_id_by_answer_id(answer_id)
        data_manager.delete_view(question_id['question_id'])
        return redirect(url_for('display_question', question_id=question_id['question_id']))


@app.route('/answer/<int:answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'GET':
        question = data_manager.get_question_by_id(
            f'(SELECT question_id FROM answer WHERE id = {answer_id})')
        answer = data_manager.get_answers_by_id(answer_id)
        return render_template('add_answer.html', post=question[0], answer=answer[0])
    elif request.method == 'POST':
        fileitem = request.files["filename"]
        filename = connection.add_file(fileitem)
        message = request.form['message']
        question_id = data_manager.edit_answer(answer_id, message, filename)
        return redirect(url_for('display_question', question_id=question_id['question_id']))


@app.route('/question/<int:question_id>/delete')
def del_question(question_id):
    if session == {}:
        return redirect(url_for('login'))
    data_manager.del_question(question_id)
    return redirect(url_for('route_list'))


@app.route('/question/<int:question_id>/<int:tag_id>/delete_tag', methods=['POST'])
def del_tag_from_question(question_id, tag_id):
    if session == {}:
        return redirect(url_for('login'))
    data_manager.delete_view(question_id)
    data_manager.del_tag_from_question(question_id, tag_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/answer/<int:answer_id>/delete', methods=['POST'])
def del_answer(answer_id):
    if session == {}:
        return redirect(url_for('login'))
    question_id = data_manager.del_answer(answer_id)
    data_manager.delete_view(question_id['question_id'])
    return redirect(url_for('display_question', question_id=question_id['question_id']))


@app.route('/comment/<int:comment_id>/delete')
def del_comment(comment_id):
    if session == {}:
        return redirect(url_for('login'))
    question_id = data_manager.del_comment(False, False, comment_id)
    data_manager.delete_view(question_id['question_id'])
    return redirect(url_for('route_list'))


@app.route('/comment_to_answer/<int:comment_id>/delete/<int:question_id>')
def del_comment_to_answers(comment_id, question_id):
    if session == {}:
        return redirect(url_for('login'))
    data_manager.del_comment(False, False, comment_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/search', methods=['POST'])
def search():
    search_item = request.form['search']
    questions = data_manager.search_question(search_item)
    if questions == []:
        questions = data_manager.search_answers(search_item)
        return render_template('list.html', headers=data_manager.SORT_QUESTION_HEADERS, posts=questions)
    else:
        return render_template('list.html', headers=data_manager.SORT_QUESTION_HEADERS, posts=questions)


@app.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    if session == {}:
        return redirect(url_for('login'))
    comment = data_manager.get_comment_by_id(comment_id)
    answer = None
    if request.method == 'GET':
        if comment[0]['answer_id'] != None:
            answer = data_manager.get_answers_by_id(
                f'(SELECT answer_id FROM comment WHERE id = {comment_id})')[0]
            question = data_manager.get_question_by_id(answer['question_id'])
        else:
            question = data_manager.get_question_by_id(
                f'(SELECT question_id FROM comment WHERE id = {comment_id})')
        return render_template('add_comment.html', comment=comment[0], post=question[0], answer=answer)
    elif request.method == 'POST':
        message = request.form['message']
        comment_id = data_manager.edit_comment(comment_id, message)
        if comment[0]['answer_id'] != None:
            answer = data_manager.get_answers_by_id(
                f'(SELECT answer_id FROM comment WHERE id = {comment_id["id"]})')
            question_id = answer[0]['question_id']
            return redirect(url_for('display_question', question_id=question_id))
        else:
            return redirect(url_for('route_list'))


@app.route('/users')
def users_list():
    users_container = data_manager.get_users_list()
    return render_template('user_list.html', user_list=users_container)


@app.route('/users/<int:user_id>')
def user_info(user_id):
    user = data_manager.get_user_by_user_id(user_id)
    questions = data_manager.get_questions_by_user_id(user_id)
    answers = data_manager.get_answers_by_user_id(user_id)
    comments = data_manager.get_comments_by_user_id(user_id)
    tags = data_manager.get_tags()
    profile_tag = data_manager.get_all_tags()
    return render_template('profile.html', user=user, questions=questions, answers=answers, comments=comments,
                           tags=tags, profile_tag=profile_tag)


@app.route('/tags')
def tag_list():
    tags = data_manager.get_tags_quantity_by_question()

    return render_template('tags.html', tags=tags)


if __name__ == "__main__":
    app.run(debug=True)
