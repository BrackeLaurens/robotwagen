import socketpool
import wifi
import time
import board
import digitalio
import pico.team510.rijden as rijden

from adafruit_httpserver import Server, Request, Response, GET, Websocket

score = 0
last_score_sent = time.monotonic()

previous_state = False  # Neem aan dat de motor eerst uit is

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
            if data == 'start':
                rijden.go() # test
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
                rijden.motorR_uit()
                rijden.motorL_uit()
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
        # Stap 1: Voeg de logica toe om de score alleen te verhogen als de waarde verandert
        # Voorbeeld: stel dat de waarde van een motor een boolean is (True/False)
        motor_state = rijden.grijp()  # Bijv. de status van de motor zorg dat de functie in rijden bestaat

        # Als de staat van de motor verandert (True naar False of andersom), verhoog de score
        if motor_state != previous_state:
            score += 100
            previous_state = motor_state  # Update de vorige staat

        # Stap 2: Stuur de score naar de webapp elke 2 seconden
        if websocket is not None and (time.monotonic() - last_score_sent) > 2:
            websocket.send_message(f"score:{score}", fail_silently=True)
            last_score_sent = time.monotonic()
    time.sleep(0.1)
