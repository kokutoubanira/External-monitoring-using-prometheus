from flask import Flask, request
app = Flask(__name__)

import datetime
from datetime import date
from redminelib import Redmine
from redminelib.exceptions import ResourceNotFoundError
import pprint
import psycopg2
import psycopg2.extras
from flask import jsonify

def connect():
    con = psycopg2.connect("host=" + "db" +
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

@app.route("/tiket", methods=['POST', 'GET'])
def get_tiket():
    dict_result = output_choice_values()
    dict_priority = [i  for i in dict_result if i["type"] == "IssuePriority"]
    dict_documentcategory = [i  for i in dict_result if i["type"] == "DocumentCategory"]
    print(dict_priority, dict_documentcategory)
    return '', 200, {}

@app.route("/gettiket", methods=["POST", "GET"])
def gettiket():
    redmine = Redmine('http://redmine:3000', key='671e27b1ea1bb634286a4840d30bb46cf9a7b468')
    issues = redmine.issue.all(sort='category:desc')
    dict_issue_list = []
    for issue in issues:
        dict_issue_list.append(dict(issue))
    return jsonify({'issue': dict_issue_list})

def tiket_create(get_reqyest):
    redmine = Redmine('http://redmine:3000', key='671e27b1ea1bb634286a4840d30bb46cf9a7b468')
    issue = redmine.issue.new()
    issue.project_id = 1
    issue.subject = 'Server Error'
    issue.tracker_id = 1     #トラッカー
    issue.description = get_reqyest["alerts"][0]["annotations"]["description"]
    issue.status_id = 1      #ステータス
    issue.priority_id = 5   #優先度
    issue.assigned_to_id = 1 #担当者のID
    issue.start_date = date.today() #開始日
    issue.save()

def comp_tiket(get_reqyest):
    redmine = Redmine('http://redmine:3000', key='671e27b1ea1bb634286a4840d30bb46cf9a7b468')
    
    target_issue = redmine.project.get('test')
    otv = output_choice_values(query="select * from issue_statuses")
    
    position_id = 1

    for i in otv:
        if i["name"] == "終了":
            position_id = i["id"]

    issues_id = {}
    for i in target_issue.issues:
        issues_id[i.id] = i
    iID = []
    for i in issues_id.keys():
        iID.append(i)
    issue = redmine.issue.get(issues_id[max(iID)].id)
    issue.status_id = position_id
    issue.done_ratio = 100
    issue.save()

@app.route("/", methods=['POST', 'GET'])
def index():
    get_reqyest = request.json

    if get_reqyest["status"] == "firing":
        tiket_create(get_reqyest)
    else :
        comp_tiket(get_reqyest)
  
    return '', 200, {}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9084)