from flask import Flask, request, redirect, url_for
from ping3 import ping


all_servers = []
ready_server = None

server_app = Flask(__name__)

@server_app.route('/api/server_init', methods=['POST'])
def receive_data():
    data = request.get_json()
    all_servers.append(data['ip'])
    ping_server(data)
    return 'Success!', 200

@server_app.route('/DeServer')
def redirect_user():
    if ready_server != None:
        return redirect(ready_server)
    # Loop them until a valid server appears if no server appeared initially, this is only nessecary for the demo
    # as redundancy is less resiliant
    return redirect(url_for('DeServer'))

def ping_server(server: str):
    time = ping(server)
    all_servers.remove(server)
    if time != None:
        all_servers.insert(server, 0)
        ready_server = server
        ping_server(server)

server_app.run(debug=True, port=8000)