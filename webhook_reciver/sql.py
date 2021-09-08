import psycopg2

def connect():
    con = psycopg2.connect("host=" + "localhost" +
                           " port=" + "5432" +
                           " dbname=" + "postgre" +
                           " user=" + "postgre" +
                           " password=" + "example")

    return con

con = connect()
sql =  'select * from enumerations'

def select_execute(con, sql):
    with con.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    return rows

res = select_execute(con, sql)
for r in res:
    print(r)
