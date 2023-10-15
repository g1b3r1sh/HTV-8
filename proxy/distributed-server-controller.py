from flask import Flask, request, redirect


all_servers = []
ready_server = None

server_app = Flask(__name__)

@server_app.route('/api/server_init', methods=['POST'])
def receive_data():
    data = request.get_json()
    servers.append(data['ip'])
    print(servers)
    return 'Success!', 200

@server_app.route('/DeServer')
def redirect_user():
    if len(servers) > 0:
        return redirect(servers[0])
    return 'No servers available (temporarily)'s

server_app.run(debug=True, port=8000)