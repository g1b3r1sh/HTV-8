import socket
import threading
import uuid

import docker

import requests
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout

API_ENDPOINT = "http://192.168.15.195:8000/"

# your API key here
API_KEY = "XXXXXXXXXXXXXXXXX"  # todo: change this

current_docker_container_id = None


def launch_docker_container(image_filename):
    with open(f"dockers/{image_filename}", 'rb') as file:
        client = docker.from_env()
        image = client.images.load(file)[0]
        container = client.containers.run(image.id, detach=True, auto_remove=True, ports={'5000/tcp': 8000})

        if container is not None:
            # Save container id to global variable
            global current_docker_container_id
            current_docker_container_id = container.id


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
        hostname = socket.getfqdn()
        ip_address = socket.gethostbyname(hostname)

        mac_address = uuid.getnode()
        mac_address_hex = ':'.join(
            ['{:02x}'.format((mac_address >> elements) & 0xff) for elements in range(0, 8 * 6, 8)][::-1])

        print(ip_address)
        print(mac_address_hex)

        data = {'dev_key': API_KEY,
                'my_mac': mac_address_hex,
                'ip': ip_address}

        send_ip_request = requests.post(url=API_ENDPOINT + 'api/server_init', json=data, headers={
            'Content-Type':'application/json'})

        # response = send_ip_request.text

        if not (send_ip_request.status_code == 200):
            return

        # app.device_num = response['device_num']
        # docker_url = response['docker_url']

        # get_docker_request = requests.get(docker_url, allow_redirects=True)

        # if docker_url.find('/'):
        #     filename = docker_url.rsplit('/', 1)[1]
        # else:
        #     filename = "docker_file.tar"

        # file = open(f"dockers/{filename}", 'wb')
        # file.write(get_docker_request.content)
        # file.close()

        # filename = "docker_file.tar"
        #
        # docker_running_thread = threading.Thread(target=launch_docker_container, args=(filename, ))
        # docker_running_thread.start()

        # change page
        app.root.transition = FadeTransition()
        app.root.current = "stop_service"


class StopServicePage(BoxLayout):
    def stop_service(self):
        status = self.kill_docker_container(current_docker_container_id)

        if status:
            # Switch to the registration screen
            app.root.transition = FadeTransition()
            app.root.current = 'start_service'

    def update_label(self, dt):
        self.amount += 0.01
        self.ids.dynamic_label.text = f'${self.amount:.2f}'

    def kill_docker_container(self, container_id):
        # Stop docker process and cleanup docker files
        client = docker.from_env()
        if current_docker_container_id is not None:
            client.containers.get(container_id).kill()
            return True
        # Note: Check if image had already existed before being added to docker to avoid removing pre-existing images
        # client.images.remove(current_docker_image_id)

        return False


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
        sm.add_widget(start_service_screen)
        sm.add_widget(registration_screen)
        sm.add_widget(login_screen)
        sm.add_widget(stop_service_screen)
        # sm.add_widget(start_service_screen)
        return sm


if __name__ == '__main__':
    app = ServerApp()
    app.run()
