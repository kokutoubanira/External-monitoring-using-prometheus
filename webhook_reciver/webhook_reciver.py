import json
import logging
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from jira import JIRA # install this package by pip in advance

logging.basicConfig(level=logging.DEBUG, format="%(asctime)-15s %(message)s")
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

class TroubleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))

        alert_data = self.build_alert_data(data)
        logging.info("recieved data:%s" % alert_data)
        self.create_alert_jira_issue(alert_data, data["status"])

    def build_alert_data(self, data):
        # customize by your metrics
        alert_data = {
            "status": data["status"],
            "alertname": data["alerts"][0]["labels"]["alertname"],
            "starts_at": data["alerts"][0]["startsAt"],
            "summary": data["alerts"][0]["annotations"]["summary"],
            "group_key": data["groupKey"]
        }
        return alert_data

    def create_alert_jira_issue(self, alert_data, alert_status):
        j = JiraPoster()
        j.create_alert_jira(alert_data)

class JiraPoster():
    def __init__(self):
        # fill your JIRA info
        server = "https://***********.atlassian.net/"
        basic_auth = ('*************', '***********')
        self.jira = JIRA(server=server, basic_auth=basic_auth)

    def create_alert_jira(self, data):
        # customize as you want
        issue_dict = {
            'project': {"key": "TEST"},
            'summary': "[ALERT] %s" % data["summary"],
            'description': "h4.alertname\n%s\nh4.starts at\n%s\nh4.summary\n%s\nh4.group key\n%s" % (data["alertname"], data["starts_at"], data["summary"], data["group_key"]),
            'issuetype': {'name': 'Task'},
        }
        if data["status"] == "firing":
                self.jira.create_issue(fields=issue_dict)

if __name__ == "__main__":
    httpd = HTTPServer(('', 9083), TroubleHandler)
    httpd.serve_forever()
