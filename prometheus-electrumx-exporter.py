from flask import Flask, send_file, request, Response
from prometheus_client import start_http_server, Counter, generate_latest, Gauge
import subprocess
#import logging

#logger = logging.getLogger(__name__)

app = Flask(__name__)

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')
 
ELECTRUMX_USERS = Gauge('electrumx_connected_clients', 'Number of currently connected clients')
ELECTRUMX_TXS = Gauge('electrumx_transactions_sent', 'Number of transactions sent')
ELECTRUMX_ERRORS = Gauge('electrumx_connection_errors', 'Number of client connection errors')

@app.route('/metrics', methods=['GET'])
def get_data():
    getinfo = subprocess.run(['/usr/bin/electrumx-rpc', 'getinfo'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    info = getinfo.splitlines()
    for line in info:
        if "count\":" in line:
            ELECTRUMX_USERS.set(int(''.join(i for i in line if i.isdigit())))
        if "txs sent" in line:
            ELECTRUMX_TXS.set(int(''.join(i for i in line if i.isdigit())))
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
 
if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0')
    app.run(port=8003)
