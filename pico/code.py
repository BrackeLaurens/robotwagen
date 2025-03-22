import socketpool
import wifi
import time
import board
import digitalio

from adafruit_httpserver import Server, Request, Response, GET, Websocket

SSID = "PICO-TEAM-510"  # Verander X naar groepsnummer
PASSWORD = "CENTRIS123"  # Verander voor veiligheidsredenen

wifi.radio.start_ap(ssid=SSID, password=PASSWORD)

# print IP adres
print("My IP address is", wifi.radio.ipv4_address_ap)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)
websocket = None
led_blinking = False
led_state = False
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

@server.route("/connect-test", GET)
def connect_test(request: Request):
    global led_blinking  # Use the global variable
    led_blinking = True  # Set the flag to start blinking

@server.route("/connect-stop", GET)
def connect_stop(request: Request):
    global led_blinking  # Use the global variable
    led_blinking = False  # Set the flag to stop blinking

# Deze functie wordt uitgevoerd wanneer de server een HTTP request ontvangt
@server.route("/connect-websocket", GET)
def connect_client(request: Request):
    global websocket  # pylint: disable=global-statement

    if websocket is not None:
        websocket.close()  # Close any existing connection

    websocket = Websocket(request)

    return websocket

server.start(str(wifi.radio.ipv4_address_ap), 80)

while True:
    server.poll()

    # Check the led_blinking flag to control the LED
    if led_blinking:
        led_sate = not led_state
        led.value = led_state

    if websocket is not None:
        data = websocket.receive(fail_silently=True)
        if data is not None:
            print(data)
            websocket.send_message(data, fail_silently=True)
    time.sleep(0.1) 
