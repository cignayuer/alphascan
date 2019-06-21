import sqlite3 as sq

started = False
c_cursor = None


def start(db: str = 'test.db'):
    global conn
    try:
        conn = sq.connect(db)
        global c_cursor
        c_cursor = conn.cursor()
        global started
        started = True
    except Exception as e:
        print(e)
        global c_cursor
        c_cursor = None
        global started
        started = False
    return c_cursor


def create_table(name: str, value_list: list, auto=True):
    if auto:
        start()
    if c_cursor is None:
        return None
    c_cursor.excute('CREATE TABLE %s (%s);' % (name, value_list))


def end():
    conn.commit()
    conn.close()
