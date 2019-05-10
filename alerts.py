#!/usr/bin/python3

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import datetime

db_connect = create_engine('sqlite:///alerts.db')
app = Flask(__name__)
api = Api(app)

now = datetime.datetime.now()


def create_db():
    conn = db_connect.connect()  # connect to database
    query = conn.execute('create table alerts(datetime text, description text)')
    conn.close()


class Alarm(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select datetime, description from alerts;")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

    def post(self):
        conn = db_connect.connect()
        print(request.json)
        vDateTime = now.strftime("%Y-%m-%d %H:%M")
        vDescription = request.json['description']

        query = conn.execute("insert into alerts values('" + vDateTime + "','" + vDescription + "');")
        return {'status': 'success'}


api.add_resource(Alarm, '/alarm')

# create_db();
if __name__ == '__main__':
    app.run(host='0.0.0.0')
