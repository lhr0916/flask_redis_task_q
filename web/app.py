from rq import Queue
from rq.job import Job

from worker.worker import conn

from flask import Flask, json, jsonify, render_template, request
from datetime import datetime
from urlparse import urlparse, parse_qs
import os

app = Flask(__name__)
#app.config.from_object(os.environ['APP_SETTINGS'])
#db = SQLAlchemy(app)

q = Queue(connection=conn)
print("1 app...start")
print( len(q))
print("2 app...start")
#from models import *

@app.route('/')
def index():
    return "hello world!"

@app.route('/save/<name>')
def save(name):
    data = {
            "age":30,
            "name":name,
            "cdate": datetime.now()
        }

    #db.member.insert(data)

    # job = q.enqueue(takes_a_while, 'do it')
    job = q.enqueue_call(
        func=takes_a_while, args=(data,), result_ttl=5000
    )
    print(job.get_id())
    # print(job.is_finished)
    # print(job.get_status)
    print(job.result)

    #return render_template('index.html', results=results)
    return name;

def takes_a_while(echo):
    import time
    time.sleep(1)
    print("---------------- here!! --------------")
    return echo


def user_save_from_q(json_data):
    print(json_data['name'])
    return json_data;

if __name__ == '__main__':
    port=5500
    is_debug = False
    app.run(debug=is_debug, host="0.0.0.0", port=port, threaded=True)
