SQL_USERS = """
    SELECT
        name,
        email
    FROM
        users
    WHERE
        name = %(name)s
"""
