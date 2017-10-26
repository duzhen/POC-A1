
#build a running REST API using
# python
#Flask web framework 
#Flask Restful extension

# prepare the data

# $ virtualenv venv
# $ source venv/bin/activate
# $ pip install requirements.txt

from flask import Flask, request, send_file, abort
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from rfq_pb2 import Request, Quote, LRequest
import time
import io
import json

app = Flask(__name__)
flask_api = Api(app)

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

def getProtoResponse(a,b,c):
    q = Quote()
    q.period.append(a)
    q.period.append(b)
    q.price = c
    return q.SerializeToString()

def getProtoDatabase():
    l = LRequest()
    for d in database:
        r = l.request.add()
        r.id = d['id']
        r.account = d['account']
        r.number = d['number']
        r.category = d['category']
        r.quantity = d['quantity']

    return send_file(
                io.BytesIO(l.SerializeToString()),
                mimetype='application/octet-stream')

@app.route('/')
def index():
    return "Assignment 1<p>" \
           "/rfq    show all the data<p>" \
           "/rfq/id get specific quote"

class rfq(Resource):
    def get(self):
        if 'octet-stream' in request.headers.get('Accept') and \
                        'octet-stream' in request.headers.get('Content-Type'):
            return getProtoDatabase()
        else:
            return jsonify(database)

    def post(self):
        if 'octet-stream' in request.headers.get('Accept') and \
                        'octet-stream' in request.headers.get('Content-Type'):
            rfq = Request()
            print("Post Protocol Buffer Request:")
            print(request.data)
            rfq.ParseFromString(request.data)
            print("->")
            print(rfq)

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

            p =  getProtoResponse(time.asctime(time.localtime(abs(d['id'] - 24 * 3600))),
                                    time.asctime(time.localtime(abs(d['id']))), d['number'] + d['quantity'])
            return send_file(
                io.BytesIO(p),
                mimetype='application/octet-stream')
        else:
            rfq = json.loads(request.data)
            print("Post Json Request:")
            print(request.data)
            print("->")
            print(rfq)
            data = [d for d in database if d['id'] == rfq['id']]
            if len(data) != 0:
                abort(400)
            d = {
                'id': rfq['id'],
                'account': rfq['account'],
                'number': rfq['number'],
                'category': rfq['category'],
                'quantity': rfq['quantity']
            }
            database.append(d)
            return jsonify({'price': d['number'] + d['quantity'],
                        'period': [time.asctime(time.localtime(abs(d['id'] - 24 * 3600))),
                                   time.asctime(time.localtime(abs(d['id'])))]})

    def put(self):
        if 'octet-stream' in request.headers.get('Accept') and \
                        'octet-stream' in request.headers.get('Content-Type'):
            rfq = Request()
            print("Put Protocol Buffer Request:")
            print(request.data)
            rfq.ParseFromString(request.data)
            print("->")
            print(rfq)
            data = [d for d in database if d['id'] == rfq.id]
            if len(data) == 0:
                abort(400)

            d = data[0]
            d['account'] = rfq.account
            d['number'] = rfq.number
            d['category'] = rfq.category
            d['quantity'] = rfq.quantity

            p = getProtoResponse(time.asctime(time.localtime(abs(d['id'] - 24 * 3600))),
                                 time.asctime(time.localtime(abs(d['id']))), d['number'] + d['quantity'])
            return send_file(
                io.BytesIO(p),
                mimetype='application/octet-stream')
        else:
            rfq = json.loads(request.data)
            print("Post Json Request:")
            print(request.data)
            print("->")
            print(rfq)
            data = [d for d in database if d['id'] == rfq['id']]
            if len(data) == 0:
                abort(400)

            d = data[0]
            d['account'] = rfq['account']
            d['number'] = rfq['number']
            d['category'] = rfq['category']
            d['quantity'] = rfq['quantity']

            return jsonify({'price': d['number'] + d['quantity'],
                            'period': [time.asctime(time.localtime(abs(d['id'] - 24 * 3600))),
                                       time.asctime(time.localtime(abs(d['id'])))]})

    def delete(self):
        if 'octet-stream' in request.headers.get('Accept') and \
                        'octet-stream' in request.headers.get('Content-Type'):
            rfq = Request()
            print("Delete Protocol Buffer Request:")
            print(request.data)
            rfq.ParseFromString(request.data)

            data = [d for d in database if d['id'] == rfq.id]
            if len(data) == 0:
                abort(400)
            print("Delete ID:" + str(rfq.id))

            d = data[0]
            database.remove(data[0])
            p = getProtoResponse(time.asctime(time.localtime(abs(d['id'] - 24 * 3600))),
                                 time.asctime(time.localtime(abs(d['id']))), d['number'] + d['quantity'])
            return send_file(
                io.BytesIO(p),
                mimetype='application/octet-stream')
        else:
            rfq = json.loads(request.data)
            print("Post Json Request:")
            print(request.data)
            print("->")
            print(rfq)
            data = [d for d in database if d['id'] == rfq['id']]
            if len(data) == 0:
                abort(400)
            print("Delete ID:"+str(rfq['id']))

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
        if 'octet-stream' in request.headers.get('Accept') and \
                        'octet-stream' in request.headers.get('Content-Type'):
            p = getProtoResponse(time.asctime(time.localtime(abs(d['id'] - 24 * 3600))),
                                 time.asctime(time.localtime(abs(d['id']))), d['number'] + d['quantity'])
            return send_file(
                io.BytesIO(p),
                mimetype='application/octet-stream')
        else:
            return jsonify({'price': d['number'] + d['quantity'],
                            'period': [time.asctime(time.localtime(abs(d['id'] - 24 * 3600))),
                                       time.asctime(time.localtime(abs(d['id'])))]})

flask_api.add_resource(rfq, '/rfq')
flask_api.add_resource(rfq_id, '/rfq/<int:id>')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port='5002', threaded=True)
