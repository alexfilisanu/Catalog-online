# import psycopg2
#
# conn = psycopg2.connect("dbname=postgres user=postgres password=postgres host=localhost")
# cursor = conn.cursor()
#
# cursor.execute('CALL get_all_students_above_avg_in_subject(%s, %s, %s)', (8, 'Matematica', 0))
# print(cursor.fetchall())
#
# cursor.execute('CALL get_all_students_above_avg_in_subject(%s, %s, %s)', (9, 'Matematica', 0))
# print(cursor.fetchall())
#
# cursor.execute('CALL get_class_with_most_absences_in_subject(%s, %s)', ('Matematica', ''))
# print(cursor.fetchall())
#
# cursor.execute('CALL get_class_with_most_absences_in_subject(%s, %s)', ('Romana', ''))
# print(cursor.fetchall())
#
# cursor.execute('CALL count_students_without_any_absence(%s)', (0,))
# print(cursor.fetchall())
#
# conn.commit()
# cursor.close()

from flask import Flask, render_template, request, redirect, url_for, session
from database.connection import connect_to_db
from database.actions.reports import get_report_data, get_total_students
from database.auth import authenticate_user

app = Flask(__name__)
app.secret_key = 'strong_secret_key'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

        user_role = authenticate_user(email, password)

        if user_role:
            session['username'] = email
            session['role'] = user_role
            return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        role = session.get('role')

        if role == 'elev':
            return render_template('elev_dashboard.html')
        elif role == 'profesor':
            return render_template('profesor_dashboard.html')

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/students_above_avg_in_subject', methods=['GET', 'POST'])
def students_above_abg_in_subject():
    conn = None
    cursor = None

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        if request.method == 'POST':
            subject = request.form['subject']
            grade = int(request.form['grade'])

            report_data = get_report_data(cursor, 'get_all_students_above_avg_in_subject',
                                          grade, subject, 0)
            total_students = get_total_students(cursor)

            report_data_strings = [", ".join(map(str, row)) for row in report_data]

            return render_template('students_above_avg_in_subject.html', reports=report_data_strings,
                                   total_students=total_students)

        return render_template('students_above_avg_in_subject.html', reports=None,
                               total_students=None)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)
