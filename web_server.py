import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
import rp2
import sys


ssid = 'JBAwifi'
password = 'Palmer2!'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(2)
        pico_led.on()
        sleep(0.2)
        pico_led.off()
        sleep(0.2)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    pico_led.on()
    print("returning ip")
    return ip

def open_socket(ip):
    # Open a socket
    print("in open_socket")
    address = (ip, 80)
    connection = s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("Connection is: ", connection)
        print("Address is: ", address)
        connection.bind(address)
    except:
        print("Caught exception")
        socket.reset()
        connection = socket.socket()
        connection.bind(address)
        #connection
        
    
        
    connection.listen(1)
    return connection

def webpage(temperature, state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <form action="./close">
            <input type="submit" value="Stop server" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature} degrees F</p>
            </body>
            </html>
            """
    return str(html)
    
def serve(connection):
    #Start a web server
    print("In serve()")
    state = 'ON'
    pico_led.on()
    temperature = 0
    while True:
        client = connection.accept()[0]
        print("Sccepted client connection")
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
            print("Split client request")
        except IndexError:
            pass
        if request == '/lighton?':
            print("requested light on")
            pico_led.on()
            state = 'ON'
        elif request =='/lightoff?':
            print("requested light off")
            pico_led.off()
            state = 'OFF'
        elif request == '/close?':
            print("request to close session received")
            sys.exit()
        temperature = pico_temp_sensor.temp * 9/5 + 32
        html = webpage(temperature, state)
        client.send(html)
        client.close()


ip = connect()
print("wifi connection setup complete")
connection = open_socket(ip)
print("finished socket setup")
serve(connection)
    
