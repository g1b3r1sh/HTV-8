import socket

import requests
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout

API_ENDPOINT = "http://pastebin.com/api/api_post.php"  # todo: change this

# your API key here
API_KEY = "XXXXXXXXXXXXXXXXX"  # todo: change this


class RegistrationPage(BoxLayout):
    def go_to_login_page(self):
        # Switch to the login screen
        app.root.current = 'login'

    def register_user(self, name, email, password, comp_name):
        print(name, email, password, comp_name)


class LoginPage(BoxLayout):
    def go_to_registration_page(self):
        # Switch to the registration screen
        app.root.current = 'registration'

    def login_user(self, email, password):
        if email == "htk@htk.com" and password == "test1234":
            app.root.current = "start_service"


class StartServicePage(BoxLayout):
    def logout(self):
        # Switch to the registration screen
        app.root.current = 'login'

    def start_service(self):
        global device_num

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        print(ip_address)

        data = {'api_dev_key': API_KEY,
                'api_option': 'paste',
                'api_my_ip': ip_address,
                'api_paste_format': 'python'}

        send_ip_request = requests.post(url=API_ENDPOINT, data=data)

        response = send_ip_request.json()

        if not (send_ip_request.status_code == 200 and (response is not None or response != '')):
            return

        device_num = response['device_num']
        docker_url = response['docker_url']

        get_docker_request = requests.get(docker_url, allow_redirects=True)

        if docker_url.find('/'):
            filename = docker_url.rsplit('/', 1)[1]
        else:
            filename = "docker_file"

        file = open(f"dockers/{filename}", 'wb')
        file.write(get_docker_request.content)
        file.close()

        # Running the docker

        # change page
        app.root.transition = FadeTransition()
        app.root.current = "stop_service"


class StopServicePage(BoxLayout):
    def stop_service(self):
        # Switch to the registration screen
        app.root.transition = FadeTransition()
        app.root.current = 'start_service'


class ServerApp(App):
    device_num = "Device number 1"

    def build(self):
        sm = ScreenManager()

        # Page initialization
        registration_screen = Screen(name='registration')
        registration_screen.add_widget(RegistrationPage())
        login_screen = Screen(name='login')
        login_screen.add_widget(LoginPage())
        start_service_screen = Screen(name='start_service')
        start_service_screen.add_widget(StartServicePage())
        stop_service_screen = Screen(name='stop_service')
        stop_service_screen.add_widget(StopServicePage())

        # Adding pages to the screen manager
        sm.add_widget(registration_screen)
        sm.add_widget(login_screen)
        sm.add_widget(stop_service_screen)
        sm.add_widget(start_service_screen)
        return sm


if __name__ == '__main__':
    app = ServerApp()
    app.run()
