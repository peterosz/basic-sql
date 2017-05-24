from flask import Flask, render_template
import data_manager


app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/all-school')
def show_all_school():
    return data_manager.all_school()


@app.route('/mentors-by-country')
def show_mentors_by_country():
    return data_manager.mentors_by_country()


@app.route('/contacts')
def show_contacts():
    return data_manager.contacts()


@app.route('/applicants')
def show_applicants():
    return data_manager.applicants()


@app.route('/applicants-and-mentors')
def show_applicants_and_mentors():
    return data_manager.applicants_and_mentors()


if __name__ == '__main__':
    app.run(debug=True)
