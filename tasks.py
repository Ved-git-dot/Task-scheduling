import requests
from celery import Celery
import pytz
from skyfield.api import load, EarthSatellite, wgs84, utc
from datetime import datetime, timedelta, timezone
import socket

address = ('localhost', 5001)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(address)


def send_command(cli_sock, data):
    cli_sock.sendall(data.encode("utf-8"))
    response = cli_sock.recv(1024).decode("utf-8")
    print(response)



app = Celery('tasks')
app.config_from_object('celeryconfig')

@app.task
def tle(fetch=True):
    if not fetch:
        print("TLE not fetched")
        return
    url="https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"

    response = requests.get(url)
    if response.status_code == 200:
        with open("tle.txt", "w") as file:
            file.write(response.text)
        print("Data written to tle.txt")
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

@app.task
def initiate_pass():
    print("GPIO pins ON")

@app.task
def generate_the_text_files():
    response = send_command(client_socket, 'generate_data')
    print("TEXT FILES FOR THE CONTROLLERS GENERATED", response)

@app.task
def switch_on_hydra():
    response = send_command(client_socket, 'start_hydra')
    print("HYDRA ON", response)

@app.task
def switch_on_arduinos():
    response = send_command(client_socket, 'switch_on_arduino')
    print("LNA & RX GAIN BLOCK SWITCHED ON", response)

@app.task
def start_radio():
    response = send_command(client_socket, 'start_gnuradio')
    print("GNU RADIO PYTHON SCRIPT IS RUNNING", response) 

@app.task
def start_controllers():
    response = send_command(client_socket, 'start_radio')
    send_command(client_socket, 'start_rotator')
    print("RADIO AND ROTATOR CONTROLLERS ENGAGED", response) 

@app.task
def switch_off_arduinos():
    response = send_command(client_socket, 'switch_off arduino')
    print("LNA & RX GAIN BLOCK SWITCHED OFF", response) 

@app.task
def kill_pids():
    response = send_command(client_socket, 'kill_pid')
    print("HYDRA & GNU RADIO ARE STOPPED", response) 

@app.task
def switch_off_gpio():
    print("GPIO PINS ARE LOW. THE PASS IS OVER")

