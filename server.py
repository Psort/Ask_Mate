from flask import Flask, render_template

import data_manager

app = Flask(__name__)


@app.route('/')
def main():
    questions = data_manager.get_question_data()
    return render_template('excercise/main.html', questions=questions)


if __name__ == "__main__":
    app.run(debug=True)
