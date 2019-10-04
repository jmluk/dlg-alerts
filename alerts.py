#!/usr/bin/python

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import datetime
import mysql.connector

app = Flask(__name__)
api = Api(app)

now = datetime.datetime.now()

mydb = mysql.connector.connect(
   host="localhost",
   user="dlg",
   passwd="cheese",
   database="dlg"
)


class Alarm(Resource):

    def post(self):
        print(request.json)
        vDateTime = now.strftime("%Y-%m-%d %H:%M")
        vDescription = request.json['description']
        vSeverity = request.json['severity']

        query = "insert into alerts(datetime,description,severity,policy,accountname,actionname,eventType,displayname,eventTime,application,tier,node,db) values('" + vDateTime + "','" + vDescription + "','" + vSeverity + "','" + request.json['policy'] + "','" + request.json['accountname'] + "','" + request.json['actionname'] + "','" + request.json['eventType'] + "','" + request.json['displayName'] + "','" + request.json['eventTime'] + "','" + request.json['application'] + "','" + request.json['tier'] + "','" + request.json['node'] + "','" + request.json['db'] + "')"

        mycursor = mydb.cursor()
        mycursor.execute(query)
        mydb.commit()

        return 200


api.add_resource(Alarm, '/alarm')

# create_db();
if __name__ == '__main__':
    app.run(host='0.0.0.0')
