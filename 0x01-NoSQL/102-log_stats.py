#!/usr/bin/env python3
""" module for a Python script that provides
some stats about Nginx logs stored in MongoDB"""

if __name__ == '__main__':
    from pymongo import MongoClient

    # initialuze a MongoClient instance
    client = MongoClient('mongodb://127.0.0.1:27017')
    # get the nginx collection
    nginx_logs = client.logs.nginx

    # methods to check
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    # print total log count
    print(nginx_logs.count_documents({}), "logs")
    print("Methods:")

    # print count for all methods
    for method in methods:
        count = nginx_logs.count_documents({'method': method})
        print("\tmethod {}: {}".format(method, count))

    status = nginx_logs.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{status} status check")

    print("IPs:")
    ips = nginx_logs.aggregate(
            [{'$group': {
                '_id': '$ip',
                'count': {'$sum': 1}
                }
              },
                {'$sort': {'count': -1}},
                {'$limit': 10}
             ])
    for log in ips:
        print(f"\t{log['_id']}: {log['count']}")
