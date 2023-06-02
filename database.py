import sqlite3 as sq


def slc_user(username):
    conn = sq.connect("users.db")
    cursor = conn.cursor()

    sql = "select * from users where username=?"
    val = (username,)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    return result


def slc_news(username):
    conn = sq.connect("users.db")
    cursor = conn.cursor()

    sql = "select * from news"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def ins_user(username, password):
    conn = sq.connect("users.db")
    cursor = conn.cursor()

    try:
        sql = "insert into users(username,password)values(?,?)"
        val = (username, password)
        cursor.execute(sql, val)
        conn.commit()
        return True
    except:
        return False


def ins_news(title, txt):
    conn = sq.connect("users.db")
    cursor = conn.cursor()

    try:
        sql = "insert into news(title,txt)values(?,?)"
        val = (title, txt)
        cursor.execute(sql, val)
        conn.commit()
        return True
    except:
        return False


def show_user():
    conn = sq.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("select * from users")
    result = cursor.fetchall()
    return result


def show_news():
    conn = sq.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("select * from news")
    result = cursor.fetchall()
    return result
