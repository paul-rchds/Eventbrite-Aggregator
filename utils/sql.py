from django.db import connection


def dict_fetch_all(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def execute_sql(query_str):
    with connection.cursor() as cursor:
        cursor.execute(query_str)
        rows = dict_fetch_all(cursor)

    return rows
