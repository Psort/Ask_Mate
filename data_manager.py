import database_common


@database_common.connection_handler
def get_question_data(cursor):
    query = """
            SELECT *
            FROM question
            ORDER BY id
    """
    cursor.execute(query)
    return cursor.fetchall()

