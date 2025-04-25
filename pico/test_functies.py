import socketpool
import wifi
import time
import board
import digitalio
import pico.rijdentest as rijdentest

from adafruit_httpserver import Server, Request, Response, GET, Websocket

score = 0
last_score_sent = time.monotonic()

previous_state = False  # Neem aan dat de motor eerst uit is
motor_running = False #variabele voor de grijpfunctie aan te roepen als deeze true wordt

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
    if websocket is not None:
        data = websocket.receive(fail_silently=True)
        if data is not None:
            global previous_state
            # Check if the received data is "test"
            if data == 'start':

                rijdentest.go() # test
                led.value = True
                time.sleep(0.1)
                led.value = False
                time.sleep(0.1)
                led.value = True
                time.sleep(0.1)
                led.value = False
                time.sleep(0.1)
                led.value = True
                time.sleep(0.1)
                led.value = False
                websocket.send_message("success", fail_silently=True)
            elif data == "noodstop":
                rijdentest.motorR_uit()
                rijdentest.motorL_uit()
                led.value = True
                time.sleep(0.1)
                led.value = False
                time.sleep(0.1)
                led.value = True
                time.sleep(0.1)
                led.value = False
                time.sleep(0.1)
                led.value = True
                time.sleep(0.1)
                led.value = False
                websocket.send_message("success", fail_silently=True)
            else:
                websocket.send_message(data, fail_silently=True)
# live score

    time.sleep(0.1)
