from flask import Flask, jsonify
from script import run_bot

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello DATCH, Welcome!"

@app.route('/follow/<username>', methods=['GET'])
def follow(username):
    run_bot(username)
    return jsonify({"message": "Bot started following followers of {}".format(username)}), 200

if __name__ == '__main__':
    app.run()
