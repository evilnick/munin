#!/usr/env python3
import json
from flask import Flask, request, jsonify
import sqlite3
import time
import pickle

# DB connect
app = Flask(__name__)
conn = sqlite3.connect('rough.db')
c = conn.cursor()


# FLASK routes

@app.route('/')
def dash():
    return "<html><head></head><body>nin</h1><p>The crow watches</></body></html>"

    
@app.route('/git',methods=['POST'])
def git():
    data = json.loads(request.data)
    event = request.headers.get('X-Github-Event')
    print("New event - {} in repo {}".format(event,data['repository']['name']))
    c.execute("INSERT INTO events VALUES ( ? , ? )", (str(time.time()), request.data))
    conn.commit()
    handle(event,data)    
    return "OK"
# Helpers

def pack_labels(data):
    list=[]
    for x in data:
        list.append( (x['color'],x['name']) )
    return (pickle.dumps(list))
# Handlers

def handle(event,data):
    if event == 'issues':
      print('issue event')
      # log in db
      print("Action: {}".format(data['action']))
      print("Issue_url: {}".format(data['issue']['url']))
      print("Issue_id: {}".format(data['issue']['id']))
      print("Issue_number: {}".format(data['issue']['number']))
      print("Issue_title: {}".format(data['issue']['title']))
      print("User_login: {}".format(data['issue']['user']['login']))
      print("User Avatar: {}".format(data['issue']['user']['avatar_url']))
      print("labels: {}".format(data['issue']['labels']))
      print("state: {}".format(data['issue']['state']))
      print("Assigned to: {}".format(data['issue']['assignee']))
      print("Comments: {}".format(data['issue']['created_at']))
      print("Comments: {}".format(data['issue']['updated_at']))
      print("Comments: {}".format(data['issue']['closed_at']))
      print("Comments: {}".format(data['issue']['body']))
      #print("Comments: {}".format(data['comment']['html_url']))
      #print("Comments: {}".format(data['comment']['id']))
      #print("Comments: {}".format(data['comment']['user']['login']))
      #print("Comments: {}".format(data['comment']['user']['avatar_url']))
      #print("Comments: {}".format(data['comment']['created_at']))
      #print("Comments: {}".format(data['comment']['body']))
      print("Comments: {}".format(data['repository']['name']))
      print("Comments: {}".format(data['repository']['html_url']))
      x = pack_labels(data['issue']['labels'])
      
      c.execute('INSERT INTO issues VALUES (?,?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);',(
          data['issue']['url'],data['issue']['id'], data['issue']['number'],
          data['issue']['title'], data['issue']['user']['login'],
          data['issue']['user']['avatar_url'], x,
          data['issue']['state'],data['issue']['assignee'],
          data['issue']['comments'], data['issue']['created_at'],
          data['issue']['updated_at'],data['issue']['closed_at'],data['issue']['body'],
          '',0,'','','','',
          data['repository']['name'],data['repository']['html_url']
          ))
      conn.commit()
      issue_handler(data)

def issue_handler(data):
    print("action = {}".format(data['action']))


if __name__ == '__main__':
    app.run()  
