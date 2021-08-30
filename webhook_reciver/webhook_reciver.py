from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
  print(request.json)
  return '', 200, {}

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=9084)


import datetime
from redminelib import Redmine
redmine = Redmine('http://localhost/redmine', username='admin', password='admin')

issue = redmine.issue.new()
issue.project_id = 'Test1'
issue.subject = 'サブジェクト'
issue.tracker_id = 1     #トラッカー
issue.description = 'チケットの内容をしめす。\n改行もできる。'
issue.status_id = 1      #ステータス
issue.priority_id = 1    #優先度
issue.assigned_to_id = 1 #担当者のID
issue.watcher_user_ids = [1] # ウォッチするユーザのID
issue.parent_issue_id = 12     # 親チケットのID
issue.start_date = datetime.date(2014, 1, 1) #開始日
issue.due_date = datetime.date(2014, 2, 1)   #期日
issue.estimated_hours = 4   # 予想工数
issue.done_ratio = 40
issue.custom_fields = [{'id': 1, 'value': 'foo'}]
issue.uploads = [{'path': 'C:\\dev\\python3\\redmine\\test.txt'}]
issue.custom_fields = [{'id': 1, 'value': 'foo'}]
issue.save()