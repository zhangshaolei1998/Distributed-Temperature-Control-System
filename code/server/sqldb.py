import sqlite3


def create_connection(db_file=".\sql.db"):
    try:
        conn = sqlite3.connect(db_file)
    except:
        print("connection fail")
    return conn


def close_connection(conn):
    conn.close()


def db_init(conn):
    try:
        cur = conn.cursor()
        cur.execute('''
        create table rdr
        (
            message_id int,
            room_id int,
            service_id int,
            request_time time,
            request_duration int,
            fanspeed int,
            feerate float,
            fee float
        );
        create table invoice
        (
            date_in date,
            date_out date,
            total_fee float
        );
        create table report
        (
            date varchar(255),
            room_id int,
            service_id int,
            times_of_onoff int,
            duration int,
            total_fee float,
            times_of_dispatch int,
            number_of_rdr int,
            times_of_changetemp int,
            times_of_changespeed int

        );''')
    except:
        print("init fail")


def db_select(conn, attrib, table, limit):
    try:
        cur = conn.cursor()
        str = ""
        if limit:
            cur.execute("select {} from {} where {};".format(attrib, table, limit))
        else:
            cur.execute("select {} from {};".format(attrib, table))
        return cur.fetchall()
    except:
        print("select fail")


def db_delete(conn, table, limit):
    try:
        cur = conn.cursor()
        cur.execute("delete from {} where {};".format(table, limit))
    except:
        print("delte fail")


def db_update(conn, table, oprt, limit):
    try:
        cur = conn.cursor()
        cur.exeute("update {} set {} where {};".format(table, oprt, limit))
    except:
        print("update fail")


def db_insert(conn, table, value):
    try:
        cur = conn.cursor()
        cur.execute("insert into {} values {};".format(table, value))
    except:
        print("insert fail")


conn = create_connection()
db_init(conn)
close_connection(conn)

