
#build a running REST API using
# python
#Flask web framework 
#Flask Restful extension

# prepare the data

# $ virtualenv venv
# $ source venv/bin/activate
# $ pip install flask flask-jsonpify flask-sqlalchemy flask-restful
# $ pip freeze 

# run this server.py code

# http://127.0.0.1:5002/employees 
# http://127.0.0.1:5002/tracks
# http://127.0.0.1:5002/employees/8


from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
# from json import dumps
from flask.ext.jsonpify import jsonify
from flask import abort

import rfq_pb2
import time

app = Flask(__name__)
api = Api(app)

database = [
    {
        'id': 1,
        'account': 'apple',
        'number': 100,
        'category': 'A',
        'quantity': 1000
    },
    {
        'id': 2,
        'account': 'linux',
        'number': 200,
        'category': 'B',
        'quantity': 2000
    },
    {
        'id': 3,
        'account': 'windows',
        'number': 300,
        'category': 'C',
        'quantity': 3000
    },
    {
        'id': 4,
        'account': 'ios',
        'number': 400,
        'category': 'D',
        'quantity': 4000
    }
]

@app.route('/')
def index():
    return "Assignment 1<p>" \
           "/rfq    show all the data<p>" \
           "/rfq/id get specific quote"

class rfq(Resource):
    def get(self):
        return jsonify(database)
    def post(self):
        rfq = rfq_pb2.Request()
        print("Post Protocol Buffer Request:")
        print(request.data)
        rfq.ParseFromString(request.data)

        data = [d for d in database if d['id'] == rfq.id]
        if len(data) != 0:
            abort(400)

        d = {
            'id': rfq.id,
            'account': rfq.account,
            'number': rfq.number,
            'category': rfq.category,
            'quantity': rfq.quantity
        }
        database.append(d)

        return jsonify({'price': d['number'] + d['quantity'],
                        'period': [time.asctime(time.localtime(abs(d['id'] - 24 * 3600))),
                                   time.asctime(time.localtime(abs(d['id'])))]})

    def put(self):
        rfq = rfq_pb2.Request()
        print("Put Protocol Buffer Request:")
        print(request.data)
        rfq.ParseFromString(request.data)

        data = [d for d in database if d['id'] == rfq.id]
        if len(data) == 0:
            abort(400)

        d = data[0]
        d['account'] = rfq.account
        d['number'] = rfq.number
        d['category'] = rfq.category
        d['quantity'] = rfq.quantity

        return jsonify({'price': d['number'] + d['quantity'],
                        'period': [time.asctime(time.localtime(abs(d['id'] - 24 * 3600))),
                                   time.asctime(time.localtime(abs(d['id'])))]})

    def delete(self):
        rfq = rfq_pb2.Request()
        print("Delete Protocol Buffer Request:")
        print(request.data)
        rfq.ParseFromString(request.data)

        data = [d for d in database if d['id'] == rfq.id]
        if len(data) == 0:
            abort(400)
        print("Delete ID:"+str(rfq.id))

        d = data[0]
        database.remove(data[0])

        return jsonify({'price': d['number'] + d['quantity'],
                        'period': [time.asctime(time.localtime(abs(d['id'] - 24 * 3600))),
                                   time.asctime(time.localtime(abs(d['id'])))]})

class rfq_id(Resource):
    def get(self, id):
        data = [d for d in database if d['id'] == id]
        if len(data) == 0:
            abort(404)
        print("Get ID:" + str(id))
        d = data[0]
        return jsonify({'price': d['number'] + d['quantity'],
                        'period': [time.asctime(time.localtime(abs(d['id'] - 24 * 3600))),
                                   time.asctime(time.localtime(abs(d['id'])))]})

api.add_resource(rfq, '/rfq')
api.add_resource(rfq_id, '/rfq/<int:id>')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port='5002', threaded=True)
