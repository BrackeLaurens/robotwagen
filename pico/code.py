import socketpool
import wifi
import time
import board
import digitalio
#import team510.rijden as rijden

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
            # Check if the received data is "test"
            if data == "noodstop":
                
                # rijden.motorR_uit()
                # rijden.motorL_uit()
                
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
    time.sleep(0.1)
