import datetime
from redminelib import Redmine
from redminelib.exceptions import ResourceNotFoundError
import pprint
import psycopg2
import psycopg2.extras
def connect():
    con = psycopg2.connect("host=" + "localhost" +
                           " port=" + "5432" +
                           " dbname=" + "postgre" +
                           " user=" + "postgre" +
                           " password=" + "example")
    return con

def select_execute(con, sql):
    with con.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    return rows

def get_tabeledata(query='select * from enumerations'):
    con = connect()
    sql =  query
    res = select_execute(con, sql)
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute (sql)
    results = cur.fetchall()
    dict_result = []
    for row in results:
        dict_result.append(dict(row))
    return dict_result

def output_choice_values(query='select * from enumerations'):
    dict_result = get_tabeledata(query)
    print(dict_result)
    return dict_result


redmine = Redmine('http://localhost:8080', key='671e27b1ea1bb634286a4840d30bb46cf9a7b468')
target_issue = redmine.project.get('test')

print(target_issue)