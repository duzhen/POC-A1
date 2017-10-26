import requests
import rfq_pb2
import argparse
import time
import json
from random import randint

data = {
        'id': int(time.time()),
        'account': 'JSON POST NEW ACCOUNT',
        'number': randint(1, 100),
        'category': 'JSON POST NEW',
        'quantity': randint(1, 10)
}

def PostRequest(Request, id=int(time.time())):
    Request.id = id
    Request.account = 'PROTOCOL POST NEW ACCOUNT'
    Request.number = randint(1, 100)
    Request.category = 'PROTOCOL POST NEW'
    Request.quantity = randint(1, 10)

def PutRequest(Request, id=int(time.time())):
    Request.id = id
    Request.account = 'PROTOCOL PUT NEW ACCOUNT'
    Request.number = randint(1, 100)
    Request.category = 'PROTOCOL PUT NEW'
    Request.quantity = randint(1, 10)

def DelRequest(Request, id=int(time.time())):
    Request.id = id
    #Request.account = 'apple'
    #Request.number = randint(0, 100)
    #Request.category = 'C'
    #Request.quantity = randint(0, 100)

def getHeaders(args):
    if args.json:
        return {'Content-Type': 'application/json', 'Accept': 'application/json'}
    else:
        return {'Content-Type': 'application/octet-stream', 'Accept': 'application/octet-stream' }

def getData(args):
    if args.json:
        print("Request Json Value:")
        print(json.dumps(data))
        return json.dumps(data)
    else:
        print("Protocol Buffer Value:")
        print(rfq.SerializeToString())
        return rfq.SerializeToString()

parser = argparse.ArgumentParser(description="Request For Quote Client.")
subparsers = parser.add_subparsers(help='commands')
get_parser = subparsers.add_parser('get', help='executes a HTTP GET request and prints the response.')
get_parser.add_argument("ID", type=int, nargs='?', help="Request ID")
get_parser.set_defaults(which='get')

post_parser = subparsers.add_parser('post', help='executes a HTTP POST request and prints the response.')
post_parser.add_argument("ID", type=int, nargs='?', help="Request ID")
post_parser.set_defaults(which='post')

put_parser = subparsers.add_parser('put', help='executes a HTTP PUT request and prints the response.')
put_parser.add_argument("ID", type=int, nargs='?', help="Request ID")
put_parser.set_defaults(which='put')

del_parser = subparsers.add_parser('delete', help='executes a HTTP DELETE request and prints the response.')
del_parser.add_argument("ID", type=int, nargs='?', help="Request ID")
del_parser.set_defaults(which='delete')

group = parser.add_mutually_exclusive_group(required=False)
group.add_argument("--json", action="store_true", dest="json", default=False, help="Use json to make a request.")
group.add_argument("--proto", action="store_true", dest="proto", default=False, help="Use protocol buffer to make a request.")

group1 = parser.add_mutually_exclusive_group(required=False)
group1.add_argument("--standalone", action="store_true", dest="alone", default=False, help="Connect to the localhost server.")
group1.add_argument("--cloud", action="store_true", dest="cloud", default=False, help="Connect to the cloud server.")

args = parser.parse_args()

if args.alone:
    url = 'http://localhost:5002/rfq'
else:
    url = 'http://ec2-18-216-37-90.us-east-2.compute.amazonaws.com:5002/rfq'

rfq = rfq_pb2.Request()

if not hasattr(args, 'which'):
    response = requests.get(url, headers=getHeaders(args))
elif args.which == 'get':
    if args.ID:
        response = requests.get(url+'/'+str(args.ID), headers=getHeaders(args))
    else:
        response = requests.get(url, headers=getHeaders(args))
elif args.which == 'post':
    if args.ID:
        data['id'] = args.ID
        PostRequest(rfq, args.ID)
    else:
        PostRequest(rfq)
    data['account'] = 'JSON POST NEW ACCOUNT'
    data['category'] = 'JSON POST NEW'
    response = requests.post(url, data=getData(args), headers=getHeaders(args))
elif args.which == 'put':
    if args.ID:
        data['id'] = args.ID
        PutRequest(rfq, args.ID)
    else:
        PutRequest(rfq)
    data['account'] = 'JSON PUT NEW ACCOUNT'
    data['category'] = 'JSON PUT NEW'
    response = requests.put(url, data=getData(args), headers=getHeaders(args))
elif args.which == 'delete':
    if args.ID:
        data['id'] = args.ID
        DelRequest(rfq, args.ID)
    else:
        DelRequest(rfq)
    response = requests.delete(url, data=getData(args), headers=getHeaders(args))

if args.json:
    print("Response Json Value:")
else:
    print("Response Protocol Buffer Value:")
print(response.content)

if args.json:
    print("->")
    print(json.loads(response.content))
elif response.status_code == 200:
    if not hasattr(args, 'which') or (args.which=='get' and not args.ID):
        l = rfq_pb2.LRequest()
        l.ParseFromString(response.content)
        print("->")
        print(l)
    else:
        quote = rfq_pb2.Quote()
        quote.ParseFromString(response.content)
        print("->")
        print(quote)