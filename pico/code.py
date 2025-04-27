import socketpool
import wifi
import time
import board
import digitalio
import pico.team510.rijden as rijden

from adafruit_httpserver import Server, Request, Response, GET, Websocket



SSID = "PICO-TEAM-510"  # Verander X naar groepsnummer
PASSWORD = "CENTRIS123"  # Verander voor veiligheidsredenen

# Initialisatie
score = 0
motor_running = False
websocket = None

# WiFi Access Point
wifi.radio.start_ap(ssid=SSID, password=PASSWORD)
print("AP IP:", wifi.radio.ipv4_address_ap)

# Hardware
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Server setup
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static")


@server.route("/connect-websocket", GET)
def connect_client(request: Request):
    global websocket
    if websocket:
        websocket.close()
    websocket = Websocket(request)
    return websocket


server.start(str(wifi.radio.ipv4_address_ap), 80)

# Hoofdlus
while True:
    server.poll()

    # Verwerk commando's
    if websocket:
        data = websocket.receive(fail_silently=True)
        if data == 'start':
            motor_running = True
            rijden.go()
            websocket.send_message("started")

        elif data == "noodstop":
            motor_running = False
            rijden.motorR_uit()
            rijden.motorL_uit()
            websocket.send_message("stopped")

    # Score update (minimale aanpassing)
    if motor_running:
        if rijden.grijp():  # Grijpcyclus voltooid
            score += 100
            if websocket:
                websocket.send_message(f"score:{score}", fail_silently=True)

    time.sleep(0.1)