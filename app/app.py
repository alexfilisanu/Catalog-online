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

from flask import Flask, render_template, request
from database.connection import connect_to_db
from database.actions.reports import get_report_data, get_total_students

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = None
    cursor = None

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        if request.method == 'POST':
            subject = request.form['subject']
            grade = int(request.form['grade'])

            report_data = get_report_data(cursor, 'get_all_students_above_avg_in_subject', grade, subject, 0)
            total_students = get_total_students(cursor)

            report_data_strings = [", ".join(map(str, row)) for row in report_data]

            return render_template('index.html', reports=report_data_strings, total_students=total_students)

        return render_template('index.html', reports=None, total_students=None)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)
