def get_report_data(cursor, procedure_name, *params):
    cursor.execute(f'CALL {procedure_name}({", ".join(["%s" for _ in params])})', params)
    return cursor.fetchall()


def get_total_students(cursor):
    cursor.execute('SELECT COUNT(*) FROM elevi')
    return cursor.fetchone()[0]
