import requests
from celery import Celery
import pytz
from skyfield.api import load, EarthSatellite, wgs84, utc
from datetime import datetime, timedelta, timezone
import socket
from socket_client import send_command

address = ('192.168.0.156', 5001)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(address)
 

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
    send_command(client_socket, 'generate_data')
    print("TEXT FILES FOR THE CONTROLLERS GENERATED")

@app.task
def switch_on_hydra():
    send_command(client_socket, 'start_hydra')
    print("HYDRA ON")

@app.task
def switch_on_arduinos():
    send_command(client_socket, 'switch_on_arduino') 
    print("LNA & RX GAIN BLOCK SWITCHED ON")

@app.task
def start_radio():
    send_command(client_socket, 'start_gnuradio')
    print("GNU RADIO PYTHON SCRIPT IS RUNNING")

@app.task
def start_controllers():
    send_command(client_socket, 'start_radio') 
    send_command(client_socket, 'start_rotator')
    print("RADIO AND ROTATOR CONTROLLERS ENGAGED")

@app.task
def switch_off_arduinos():
    send_command(client_socket, 'switch_off arduino')
    print("LNA & RX GAIN BLOCK SWITCHED OFF")

@app.task
def kill_pids():
    send_command(client_socket, 'kill_pid')
    print("HYDRA & GNU RADIO ARE STOPPED")

@app.task
def switch_off_gpio():
    print("GPIO PINS ARE LOW. THE PASS IS OVER")
        
