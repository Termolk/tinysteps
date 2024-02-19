import json
import operator
import random

from flask import Flask, render_template, request
from flask_wtf import CSRFProtect

from Forms import BookForm, RequestForm, SortForm

app = Flask(__name__)
app.secret_key = 'super secret key'

csrf = CSRFProtect()
csrf.init_app(app)

days = {"mon": "Понедельник", "tue": "Вторник", "wed": "Среда", "thu": "Четверг", "fri": "Пятница", "sat": "Суббота",
        "sun": "Воскресенье"}

goals_dict = dict([('travel', 'Для путешествий'), ('study', 'Для школы'), ('work', 'Для работы'),
                   ('relocate', 'Для переезда'), ('programming', '‍Для программирования')])

emoji = {'travel': '⛱', 'study': '🏫', 'work': '🏢', 'relocate': '🚜', 'programming': '‍💻'}


@app.route('/')
def render_main():
    with open('teachers.json', 'r', encoding='utf8') as f:
        teachers_json = json.load(f)
    teachers = random.sample(teachers_json, 6)
    return render_template('index.html', teachers=teachers, goals_dict=goals_dict, emoji=emoji)


@app.route('/all', methods=['GET', 'POST'])
def render_all():
    with open('teachers.json', 'r', encoding='utf8') as f:
        teachers_json = json.load(f)

    teachers = random.sample(teachers_json, len(teachers_json))

    if request.method == 'GET':
        form = SortForm()
        return render_template('all.html', teachers=teachers, form=form)

    if request.method == 'POST':
        form = SortForm()
        if form.validate_on_submit():
            value = form.selectField.data

            if value == '0':
                teachers = random.sample(teachers_json, len(teachers_json))
            elif value == '1':
                teachers = sorted(teachers_json, key=operator.itemgetter("price"), reverse=True)
            elif value == '2':
                teachers = sorted(teachers_json, key=operator.itemgetter("price"))
            elif value == '3':
                teachers = sorted(teachers_json, key=operator.itemgetter("rating"), reverse=True)

            return render_template('all.html', teachers=teachers, form=form)


@app.route('/goals/<goal>')
def render_goal(goal):
    print(goals_dict)
    with open('teachers.json', 'r', encoding='utf8') as f:
        teachers = json.load(f)

    filtered_teachers = [teacher for teacher in teachers if goal in teacher['goals']]

    return render_template('goal.html', goal=goal, teachers=filtered_teachers, emoji=emoji, goals_dict=goals_dict)


@app.route('/profiles/<int:id>')
def render_profile(id):
    with open('teachers.json', 'r', encoding='utf8') as f:
        teachers_json = json.loads(f.read())
    current_teacher = teachers_json[id]


    return render_template('profile.html', teacher=current_teacher, goals=goals_dict,
                           has_available_time=has_available_time, days=days)


@app.route('/request')
def render_request():
    request_form = RequestForm()
    return render_template('request.html', form=request_form)


@app.route('/request_done', methods=['POST'])
def render_request_done():
    if request.method == 'POST':
        form = RequestForm()
        if form.validate_on_submit():
            goal = dict(form.goal.choices)[form.goal.data]
            time = dict(form.time.choices)[form.time.data]
            name = form.name.data
            phone = form.phone.data

            try:
                with open('request.json', 'r', encoding='utf8') as f:
                    request_json = json.load(f)
            except json.decoder.JSONDecodeError:
                request_json = []

            request_json.append((form.goal.data, form.time.data, name, phone))

            with open('request.json', 'w', encoding='utf8') as f:
                json.dump(request_json, f)

            return render_template('request_done.html', goal=goal, time=time, name=name, phone=phone)


@app.route('/booking/<int:id>/<day>/<time>')
def render_booking(id, day, time):
    with open('teachers.json', 'r', encoding='utf8') as f:
        teachers_json = json.loads(f.read())
    current_teacher = teachers_json[id]

    form = BookForm()

    return render_template('booking.html',
                           teacher=current_teacher, days=days, day=day, time=time,
                           form=form)


@app.route('/booking_done', methods=['POST'])
def render_booking_done():
    if request.method == 'POST':
        form = BookForm()
        if form.validate_on_submit():
            day = form.clientWeekday.data
            time = form.clientTime.data
            teacher = form.clientTeacher.data
            student = form.name.data
            phone = form.phone.data

            try:
                with open('booking.json', 'r', encoding='utf8') as f:
                    booking_json = json.load(f)
            except json.decoder.JSONDecodeError:
                booking_json = []

            booking_json.append((day, time, teacher, student, phone))

            with open('booking.json', 'w', encoding='utf8') as f:
                json.dump(booking_json, f)

            teachers_json = []
            with open('teachers.json', 'r', encoding='utf8') as f:
                teachers_json = json.load(f)

            teacher = teachers_json[int(form.clientTeacher.data)]
            teacher["free"][day][time] = False

            teachers_json[int(form.clientTeacher.data)] = teacher

            with open('teachers.json', 'w', encoding='utf8') as f:
                json.dump(teachers_json, f)

            return render_template('booking_done.html', name=student, phone=phone, day=day, days=days, time=time)


@app.errorhandler(404)
@app.errorhandler(500)
def render_error(error):
    return render_template('error.html')


def has_available_time(schedule):
    for time, available in schedule.items():
        if available:
            return True
    return False


if __name__ == '__main__':
    app.run(debug=True)
