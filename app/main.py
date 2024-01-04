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
import psycopg2

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        conn = psycopg2.connect("dbname=postgres user=postgres password=postgres host=localhost")
        cursor = conn.cursor()

        if request.method == 'POST':
            subject = request.form['subject']
            grade = int(request.form['grade'])

            # Example 1
            report_data = get_report_data(cursor, 'get_all_students_above_avg_in_subject', grade, subject, 0)
            total_students = get_total_students(cursor)

            # Convert the result to a list of strings
            report_data_strings = [", ".join(map(str, row)) for row in report_data]

            return render_template('index.html', reports=report_data_strings, total_students=total_students)

        return render_template('index.html', reports=None, total_students=None)

    finally:
        cursor.close()
        conn.close()


def get_report_data(cursor, procedure_name, *params):
    cursor.execute(f'CALL {procedure_name}({", ".join(["%s" for _ in params])})', params)
    return cursor.fetchall()


def get_total_students(cursor):
    cursor.execute('SELECT COUNT(*) FROM elevi')
    return cursor.fetchone()[0]


if __name__ == '__main__':
    app.run(debug=True)
