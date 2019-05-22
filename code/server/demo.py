from sqldb import *

conn = create_connection()
db_insert(conn, "test", "(1,'abc')")
x = db_select(conn, "*", "test", "")
print(x)
