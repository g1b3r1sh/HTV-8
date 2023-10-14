from taipy import Gui
from taipy.gui import Markdown
from taipy.gui import navigate

gui = Gui

email = ''
password = ''
sign_in_md = Markdown("""
# Sign In

<|{email}|input|label=Email|>

<|{password}|input|label=Password|password=True|on_action=log_in|>

<|Log In|button|on_action=log_in|>

Go to [Second Page](/home) for more information.

""")

bandwidth = 10
docker_image: any

dashboard_md = Markdown("""
# Dashboard

<|{upload}|slider|min=10|max=1000000|>
<|{download}|slider|min=10|max=1000000|>
<|{max_ping}|slider|min=10|max=1000000|>
<|{ram}|slider|min=10|max=1000000|>
<|{ram_clock}|slider|min=1000|max=8000|>
<|{threads}|slider|min=1|max=128|>
<|{ram}|slider|min=10|max=1000000|>
<|{cpu_clock}|slider|min=10|max=1000000|>


<|{docker_image}|file_selector|label=Docker Image|extensions=.dockerfile|>

<|{value}|toggle|lov=Active; Inactive|>

""")


pages = {
    'sign-in': sign_in_md,
    'dashboard': dashboard_md,
}

def log_in(state):
    if state.email == 'htk@htk.com' and state.password == 'test1234':
        navigate(state, 'dashboard')
        


gui(pages=pages).run()