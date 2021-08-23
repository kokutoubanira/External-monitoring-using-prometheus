from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
  print(request.json)
  return '', 200, {}

if __name__ == "__main__":
  app.run(host="172.17.0.1", port=9084)