from taipy import Gui
from taipy.gui import Markdown
from taipy.gui import navigate
import requests
import netifaces



gui = Gui

root_md = Markdown("""
# Decloud
""")

home_md = Markdown("""
#### Around the world, over **1 billion computers** stay unused for more than **10 hours** per day. That is **10 billion hours** of unused computing power.

### Decloud aims to connect those in need of computer time to those with extra computer time. By selling server time that would otherwise go unused at a discounted rate, its a win-win situation for all.

<|Sign In|button|on_action=navigate_signin|>

""")

email = ''
password = ''
sign_in_md = Markdown("""
# Sign In

<|{email}|input|label=Email|>

<|{password}|input|label=Password|password=True|>

<|Log In|button|on_action=log_in|>

""")


def generate_ram_size_strings():
    ram_sizes = []
    for i in range(128, 1000, 128):
        ram_sizes.append(f"{i} MB")
    for i in range(1, 17):
        ram_sizes.append(f"{i} GB")
    return ram_sizes
ram_sizes = generate_ram_size_strings()

max_ping = 100
num_threads = 1
ram = "128 MB"
docker_image = None

dashboard_md = Markdown("""
# Order Server

<|{max_ping}|number|label=Max Ping (ms)|>


Threads:

<|{num_threads}|slider|min=1|max=128|>

RAM:

<|{ram}|slider|lov={ram_sizes}|text_anchor=none|>


<|{docker_image}|file_selector|label=Upload Docker Image|extensions=.tar|on_action=on_upload|>


<|Order|button|on_action=on_order_server|>

""")


pages = {
    '/': root_md,
    'home': home_md,
    'client/sign-in': sign_in_md,
    'client/dashboard': dashboard_md,
}

def navigate_signin(state):
    navigate(state, 'client/sign-in')

def log_in(state):
    print('login')
    if state.email == 'htk@htk.com' and state.password == 'test1234':
        navigate(state, 'client/dashboard')

def on_upload(state):
    print(state.docker_image)
    filename = state.docker_image
    dir(state)
    with open(state.docker_image, 'rb') as f:
        r = requests.post(url, data={'pxeconfig': f.read()})

def on_order_server(state):
    print(state.max_ping)
    print(state.num_threads)
    print(state.ram)

def get_lan_ip() -> str:
    iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    return netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']

Gui(pages=pages).run(port=8080, host=get_lan_ip())

gui_thread = threading.Thread(target=run_gui)
gui_thread.start()

"""
servers = []

server_app = Flask(__name__)

@server_app.route('/api/server_init', methods=['POST'])
def receive_data():
    data = request.get_json()
    servers.append(data['ip'])
    return 'Success!', 200

#server_app.run(debug=True, port=8000)

print('after')
"""