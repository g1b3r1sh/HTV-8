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

docker_image = None
max_ping = 100

dashboard_md = Markdown("""
# Dashboard

<|{max_ping}|number|label=Max Ping (ms)|>


<|{threads}|slider|min=1|max=128|value=1000|>


<|{docker_image}|file_selector|label=Upload Docker Image|extensions=*|on_action=on_upload|>

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
    filename = state.docker_image
    # In a non demo this new docker image would be pushed to the distributed servers, however we will just be using an existing dockerfile
    # on our demo distributed servers as implementation is trivial and time consuming

def get_lan_ip() -> str:
    iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    return netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']

Gui(pages=pages).run(port=8080, host=get_lan_ip())

