import sqlite3
import datetime

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
        create table if not exists rdr
        (
            room_id int,
            operate_id int,
            day_in date,
            request_time varchar(255),
            request_duration varchar(255),
            fanspeed int,
            feerate float,
            fee float
        );''')
        cur.execute('''
        create table if not exists invoice
        (
            room_id varchar(255),
            date_in date,
            date_out date,
            total_fee float
        );''')
        cur.execute('''
        create table if not exists report
        (
            date varchar(255),
            room_id int,
            operate_id int,
            times_of_onoff int,
            duration int,
            total_fee float,
            times_of_dispatch int,
            number_of_rdr int,
            times_of_changetemp int,
            times_of_changespeed int

        );''')
        print("database init success")
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
def get_conn():
    conn = create_connection()
    return conn

def set_rdr(room_id, operate_id, day_in, duration, fanspeed, feerate, fee):
    conn = get_conn()
    cur = conn.cursor()
    request_time = datetime.datetime.now()
    cur.execution("insert into rdr values(?,?,?,?,?,?,?,?)",(roomid,operate_id,day_in,request_time,duration,fanspeed,feerate,fee))
    close_connection(conn)
def get_rdr(roomid, day_in):
    conn = get_conn()
    cur = conn.cursor()
    cur.execution("select * from rdr where roomid = ? and day_in = ?",(roomid, day_in))
    close_connection(conn)
    return cur.fetchall()
def set_invoice(room_id, day_in):
    conn = get_conn()
    cur = conn.cursor()
    cur.execution("insert into invoice(roomid, day_in) values(?,?)",(room_id,day_in))
    close_connection(conn)
def get_invoice(room_id,day_in):
    conn = get_conn()
    cur = conn.cursor()
    cur.execution("select * from invoice where room_id = ? and day_in = ?",(room_id,day_in))
    close_connection(conn)
    return cur.fetchall()
def set_report(date, times_of_onoff, operate_id, duration, total_fee, times_of_dispatch, number_of_rdr, number_of_change_time, number_of_changespeed):
    conn = get_conn()
    cursor = conn.cursor()
    cur.execution("insert into report values(?,?,?,?,?,?,?,?,?,?)",(date,room_id,operate_id,times_of_onoff,duration,total_fee,times_of_dispatch,number_of_rdr,times_of_changetemp,times_of_changespeed))
    close_connection(conn)

def get_report(list_room_id, type_report, date):
    conn = get_conn()
    cursor = conn.cursor()
    report=[]
    if type_report==0:
        for room_id in list_room_id:
            cur.execution("select * from report where room_id=? and date=?",(room_id,date))
            report.append(cur.fetchone())
    elif type_report==1:
        '''
        import datetime
    d = "2013-W26"
    r = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
    print(r)
        '''
        pass
    else:
        date1 = date+"-1-1"
        date2 = date+"-12-31"
        for room_id in list_room_id:
            cur.execution("select * from report where room_id=? and date(date) >= date(?) and date(date) <= date(?)",(room_id,date1,date2))
            report.append(cur.fetchone())
conn = create_connection()
db_init(conn)
close_connection(conn)

