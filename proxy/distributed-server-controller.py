from flask import Flask, request, redirect, url_for, jsonify
from ping3 import ping
import threading

all_servers = []
ready_server = None

server_app = Flask(__name__)


@server_app.route('/api/server_init', methods=['POST'])
def receive_data():
    data = request.json
    all_servers.append(data['ip'])
    print(data)

    ping_thread = threading.Thread(target=ping_server, args=(data['ip'],))
    return jsonify({'docker_url': 'Success!'}), 200


@server_app.route('/DeServer')
def redirect_user():
    global ready_server

    print(ready_server)
    if ready_server != None:
        return redirect(ready_server)
    # Loop them until a valid server appears if no server appeared initially, this is only nessecary for the demo
    # as redundancy is less resilient
    return redirect(url_for('redirect_user'))


def ping_server(server: str):
    global ready_server

    while True:
        time = ping(server)
        all_servers.remove(server)
        if time != None:
            all_servers.insert(0, server)
            ready_server = server
        else:
            break


server_app.run(debug=True, port=8000, host="0.0.0.0")
