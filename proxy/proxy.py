from taipy import Gui, Rest
from taipy.gui import Markdown
from taipy.gui import navigate
import requests
import netifaces
from flask import Flask, request
import threading


gui = Gui

email = ''
password = ''
sign_in_md = Markdown("""
# Sign In

<|{email}|input|label=Email|>

<|{password}|input|label=Password|password=True|on_action=log_in|>

<|Log In|button|on_action=log_in|>

Go to [Second Page](/home) for more information.
Become a part of DeCloud

""")

docker_image = None
max_ping = 100
filename = ''

dashboard_md = Markdown("""
# Dashboard

<|{max_ping}|number|label=Max Ping (ms)|>


<|{threads}|slider|min=1|max=128|value=1000|>


<|{docker_image}|file_selector|label=Upload Docker Image|extensions=*|on_action=on_upload|>

""")


pages = {
    'client/sign-in': sign_in_md,
    'client/dashboard': dashboard_md,
}

def log_in(state):
    if state.email == 'htk@htk.com' and state.password == 'test1234':
        navigate(state, '/client/dashboard')

def on_upload(state):
    print(state.docker_image)
    filename = state.docker_image
    dir(state)
    with open(state.docker_image, 'rb') as f:
        r = requests.post(url, data={'pxeconfig': f.read()})

def get_lan_ip() -> str:
    iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    return netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']

def run_gui():
    gui(pages=pages).run(port=8080, host=get_lan_ip())



server_app = Flask(__name__)

@server_app.route('/api/server_init', methods=['POST'])
def receive_data():
    data = request.get_json()
    print(data['ip'])
    return 'Success!', 200

def run_flask():
    server_app.run(debug=True, port=8000)

gui_thread = threading.Thread(target=run_gui)
#flask_thread = threading.Thread(target=run_flask)

gui_thread.start()
run_flask()
