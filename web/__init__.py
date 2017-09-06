# -*- coding: UTF-8 -*-
from flask import Flask, request, json
import config

if config.PERSISTENCE['type'] == 'redis':
    from persistence.redis_impl import Redis as persister
elif config.PERSISTENCE['type'] == 'mongo':
    from persistence.mongo_impl import Mongo as persister
else:
    from persistence.redis_impl import Redis as persister
app = Flask(__name__)
db = persister()


@app.route('/proxy', methods=['GET'])
def proxy():
    anonymity = request.args.get('anonymity', None)
    protocol = request.args.get('protocol', None)
    count = request.args.get('count', 1, int)
    query = {}
    if anonymity:
        query['anonymity'] = anonymity
    if protocol:
        query['protocol'] = protocol
    return json.jsonify(db.list(count, query=query))


@app.route('/proxy/delete', methods=['GET', 'DELETE'])
def proxy_del():
    ip = request.args.get('ip', None)
    port = request.args.get('port', None)
    protocol = request.args.get('protocol', None)

    if not ip:
        return '', 400, {'Content-Type': 'application/json'}

    proxies = db.get_keys(query={'ip': ip, 'port': port, 'protocol': protocol})

    if proxies:
        for key in proxies:
            p = {k.decode('utf-8'): v.decode('utf-8') for k, v in db.handler().hgetall(key).items()}
            db.delete(p)
            return '', 204, {'Content-Type': 'application/json'}
    else:
        return '', 400, {'Content-Type': 'application/json'}


def worker():
    app.run(host=config.WEB_API_IP, port=config.WEB_API_PORT, debug=False)
