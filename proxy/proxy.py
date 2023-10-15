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

# price = {0.1, ping <= 10; 0.10 - 0.01 * (ping / 10 - 1), 10 < ping <= 100; 0.01 - 0.0001 * (ping / 10 - 1), 100 < ping <= 500; 0.005, ping > 500}
def calculate_max_ping_price(max_ping):
    if max_ping <= 10:
        return 0.1
    if max_ping <= 100:
        return 0.1 - 0.01 * (max_ping // 10 - 1)
    if max_ping <= 500:
        return 0.01 - 0.0001 * (max_ping // 10 - 1)
    return 0.005

# price = 0.00001 * threads
def calculate_num_threads_price(num_threads):
    return 0.00001 * num_threads

# price = 0.005 / GB
def calculate_ram_price(ram):
    if ram[-2] == 'M':
        return int(ram.split()[0]) * 0.001 * 0.005
    elif ram[-2] == 'G':
        return int(ram.split()[0]) * 0.005

max_ping = 100
max_ping_price = calculate_max_ping_price(max_ping)
num_threads = 1
num_threads_price = calculate_num_threads_price(num_threads)
ram = "128 MB"
ram_price = calculate_ram_price(ram)
total_price = max_ping_price + num_threads_price + ram_price

def update_prices(state):
    state.max_ping_price = calculate_max_ping_price(state.max_ping)
    state.num_threads_price = calculate_num_threads_price(state.num_threads)
    state.ram_price = calculate_ram_price(state.ram)
    state.total_price = state.max_ping_price + state.num_threads_price + state.ram_price

docker_image = None

dashboard_md = Markdown("""
# Order Server

<|{max_ping}|number|label=Max Ping (ms)|propagate|on_change=update_prices|>

Threads:

<|{num_threads}|slider|min=1|max=128|on_change=update_prices|>

RAM:

<|{ram}|slider|lov={ram_sizes}|text_anchor=none|continuous|on_change=update_prices|>


<|{docker_image}|file_selector|label=Upload Docker Image|extensions=.tar|on_action=on_upload|>

### Checkout
<|card|
Max Ping: $<|{max_ping_price}|text|format=%.5f|>/hr

Threads: $<|{num_threads_price}|text|format=%.5f|>/hr

RAM: $<|{ram_price}|text|format=%.5f|>/hr



##### **Total: $<|{total_price}|text|format=%.5f|>/hr**

<|Order|button|on_action=on_order_server|>

|>

""")

order_complete_md = Markdown("""
# Your order has been completed

## Order details:

* Max Ping: <|{max_ping}|> ms
* Threads: <|{num_threads}|> thread(s)
* RAM: <|{ram}|>
* Price: $<|{total_price}|text|format=%.5f|>/hr

## You can visit your remotely hosted website [here]().
""")

# TODO Add hard link to proxy server


pages = {
    '/': root_md,
    'home': home_md,
    'client/sign-in': sign_in_md,
    'client/dashboard': dashboard_md,
    'client/complete': order_complete_md,
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

def on_order_server(state):
    navigate(state, 'client/complete')

def get_lan_ip() -> str:
    iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    return netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']

Gui(pages=pages).run(port=8080, host=get_lan_ip(), title='DeCloud')

