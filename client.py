import requests
import rfq_pb2
import argparse
import time
from random import randint

url = 'http://ec2-18-216-10-102.us-east-2.compute.amazonaws.com:5002/rfq'

def PostRequest(Request, id=int(time.time())):
    Request.id = id
    Request.account = 'post new account'
    Request.number = randint(1, 100)
    Request.category = 'POST NEW'
    Request.quantity = randint(1, 10)

def PutRequest(Request, id=int(time.time())):
    Request.id = id
    Request.account = 'put new account'
    Request.number = randint(1, 100)
    Request.category = 'PUT NEW'
    Request.quantity = randint(1, 10)

def DelRequest(Request, id=1):
    Request.id = id
    #Request.account = 'apple'
    #Request.number = randint(0, 100)
    #Request.category = 'C'
    #Request.quantity = randint(0, 100)

parser = argparse.ArgumentParser(description="Protocol Buffer Client.")
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

args = parser.parse_args()

rfq = rfq_pb2.Request()

if args.which == 'get':
    if args.ID:
        response = requests.get(url+'/'+str(args.ID))
    else:
        response = requests.get(url)
elif args.which == 'post':
    if args.ID:
        PostRequest(rfq, args.ID)
    else:
        PostRequest(rfq)
    response = requests.post(url, data=rfq.SerializeToString(), headers={'Content-Type': 'application/octet-stream'})
elif args.which == 'put':
    if args.ID:
        PutRequest(rfq, args.ID)
    else:
        PutRequest(rfq)
    response = requests.put(url, data=rfq.SerializeToString(), headers={'Content-Type': 'application/octet-stream'})
elif args.which == 'delete':
    if args.ID:
        DelRequest(rfq, args.ID)
    else:
        DelRequest(rfq)
    response = requests.delete(url, data=rfq.SerializeToString(), headers={'Content-Type': 'application/octet-stream'})
print("Protocol Buffer Value:")
print(rfq.SerializeToString())
print("Response Json Value:")
print(response.content)