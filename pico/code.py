import time
import board
import pwmio
import digitalio
import analogio
from adafruit_motor import servo
import socketpool
import wifi
import os
from adafruit_httpserver import Server, Request, Response, GET, Websocket
from adafruit_us100 import adafruit_hcsr04

ldr_right = analogio.AnalogIn(board.GP28)
ldr_left = analogio.AnalogIn(board.GP27)
ldr_back = analogio.AnalogIn(board.GP26)

trigger_pin = board.GP4
echo_pin = board.GP5
sonar = adafruit_hcsr04.HCSR04(trigger_pin, echo_pin)

motor_aan_uitR = pwmio.PWMOut(board.GP16, frequency=1000)
motor_richtingR = digitalio.DigitalInOut(board.GP17)
motor_richtingR.direction = digitalio.Direction.OUTPUT

motor_aan_uitL = pwmio.PWMOut(board.GP14, frequency=1000)
motor_richtingL = digitalio.DigitalInOut(board.GP15)
motor_richtingL.direction = digitalio.Direction.OUTPUT

pwm = pwmio.PWMOut(board.GP20, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)

snelheid = 40
draaisnelheid = 40
bochtcount = 0
line_count = 0
frontlinecount = 0
rijden_actief = False
grijp_actief = False

DREMPEL_ZWARTE_LIJN_links = None
DREMPEL_ZWARTE_LIJN_rechts = None
DREMPEL_ZWARTE_LIJN_achter = None
drempelzwartlinksdraai = None
drempelzwartrechtsdraai = None


def motorR_aan(speed):
    motor_aan_uitR.duty_cycle = int((speed / 100) * 65535)


def motorR_uit():
    motor_aan_uitR.duty_cycle = 0


def achteruitR():
    motor_richtingR.value = True


def vooruitR():
    motor_richtingR.value = False


def motorL_aan(speed):
    motor_aan_uitL.duty_cycle = int((speed / 100) * 65535)


def motorL_uit():
    motor_aan_uitL.duty_cycle = 0


def achteruitL():
    motor_richtingL.value = True


def vooruitL():
    motor_richtingL.value = False


def meet_ldr(ldr):
    return ldr.value * (3.3 / 65535)


def vooruit(speed):
    vooruitL()
    vooruitR()
    motorR_aan(speed)
    motorL_aan(speed)


def achteruit(speed):
    achteruitL()
    achteruitR()
    motorR_aan(speed)
    motorL_aan(speed)


def draai_rechts(speed):
    global motor_running
    achteruitR()
    vooruitL()
    motorR_aan(speed)
    motorL_aan(speed)
    time.sleep(1)
    while motor_running and meet_ldr(ldr_right) > drempelzwartrechtsdraai:
        server.poll()
        time.sleep(0.05)
    if not motor_running:
        motorR_uit()
        motorL_uit()
        return


def draai_links(speed):
    global motor_running
    achteruitL()
    vooruitR()
    motorR_aan(speed)
    motorL_aan(speed)
    time.sleep(1)
    while motor_running and meet_ldr(ldr_left) > drempelzwartlinksdraai:
        server.poll()
        time.sleep(0.05)
    if not motor_running:
        motorR_uit()
        motorL_uit()
        return


def draai_180_graden(speed):
    global motor_running
    achteruitR()
    vooruitL()
    motorR_aan(speed)
    motorL_aan(speed)
    time.sleep(0.5)
    linecount_uturn = 0
    while motor_running and linecount_uturn < 2:
        if meet_ldr(ldr_right) <= drempelzwartrechtsdraai:
            linecount_uturn += 1
            while motor_running and meet_ldr(ldr_right) <= drempelzwartrechtsdraai:
                server.poll()
                time.sleep(0.05)
        server.poll()
        time.sleep(0.05)
    if not motor_running:
        motorR_uit()
        motorL_uit()
        return


def grijp():
    global grijp_actief
    grijp_actief = True
    for angle in range(0, 175, 10):
        my_servo.angle = angle
        time.sleep(0.05)
    for angle in range(175, 0, -10):
        my_servo.angle = angle
        time.sleep(0.05)
    grijp_actief = False


def kalibreer_drempelwaardes(samples=100, margeL=0.90, margeLD=0.95, margeR=0.90, margeRD=0.95, margeA=0.90):
    global DREMPEL_ZWARTE_LIJN_links, DREMPEL_ZWARTE_LIJN_rechts, DREMPEL_ZWARTE_LIJN_achter, drempelzwartlinksdraai, drempelzwartrechtsdraai

    max_links = max_rechts = max_achter = 0
    print("Kalibratie bezig...Zet de robot op wit vlak.")

    for _ in range(samples):
        max_links = max(max_links, meet_ldr(ldr_left))
        max_rechts = max(max_rechts, meet_ldr(ldr_right))
        max_achter = max(max_achter, meet_ldr(ldr_back))
        time.sleep(0.01)

    DREMPEL_ZWARTE_LIJN_links = max_links * margeL
    DREMPEL_ZWARTE_LIJN_rechts = max_rechts * margeR
    DREMPEL_ZWARTE_LIJN_achter = max_achter * margeA
    drempelzwartlinksdraai = max_links * margeLD
    drempelzwartrechtsdraai = max_rechts * margeRD

    print(f"Max L: {max_links:.2f}V, R: {max_rechts:.2f}V, Achter: {max_achter:.2f}V")

'''
print('Begin kalibratie')
kalibreer_drempelwaardes()
print('Kalibratie voltooid.')
'''

SSID = "PICO-TEAM-510"
PASSWORD = "CENTRIS123"

wifi.radio.start_ap(ssid=SSID, password=PASSWORD)
print("AP IP:", wifi.radio.ipv4_address_ap)
print(os.listdir("/static"))
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static")

score = 0
motor_running = False
websocket = None
data = None


@server.route("/connect-websocket", GET)
def connect_client(request: Request):
    global websocket
    if websocket:
        websocket.close()
    websocket = Websocket(request)
    return websocket


server.start(str(wifi.radio.ipv4_address_ap), 80)

while True:
    server.poll()
    if sonar.distance <= 12:
        data = 'noodstop'
    if websocket:
        rec = websocket.receive(fail_silently=True)
        if rec is not None:
            data = rec
        if data == 'start':
            line_count = 0
            bochtcount = 0
            motor_running = True
            data = None
            websocket.send_message("started")
        elif data == 'noodstop':
            motor_running = False
            motorR_uit()
            motorL_uit()
            data = None
            print('NOODSTOP')
            websocket.send_message("stopped")
        elif data =='kalibreer':
            print('Begin kalibratie')
            kalibreer_drempelwaardes()
            print('Kalibratie voltooid.')
            data= None
    if motor_running:
        vooruit(snelheid)
        diff = meet_ldr(ldr_left) - meet_ldr(ldr_right)
        zwart_links = meet_ldr(ldr_left) < drempelzwartlinksdraai
        zwart_rechts = meet_ldr(ldr_right) < drempelzwartrechtsdraai
        zwart_linksF = meet_ldr(ldr_left) < DREMPEL_ZWARTE_LIJN_links
        zwart_rechtsF = meet_ldr(ldr_right) < DREMPEL_ZWARTE_LIJN_rechts
        zwart_achter = meet_ldr(ldr_back) < DREMPEL_ZWARTE_LIJN_achter

        if zwart_achter:
            line_count += 1
            print(line_count)
            while meet_ldr(ldr_back) < DREMPEL_ZWARTE_LIJN_achter:
                time.sleep(0.1)
        if zwart_linksF and zwart_rechtsF:
            frontlinecount += 1
            while meet_ldr(ldr_left) < DREMPEL_ZWARTE_LIJN_links and meet_ldr(ldr_right) < DREMPEL_ZWARTE_LIJN_rechts:
                time.sleep(0.1)
        if -0.20 < diff < 0.20:
            vooruit(snelheid)
        elif zwart_links:
            motorR_aan(snelheid + 10)
            motorL_aan(snelheid - 10)
        elif zwart_rechts:
            motorR_aan(snelheid - 10)
            motorL_aan(snelheid + 10)
        else:
            vooruit(snelheid)

        if frontlinecount == 2 and bochtcount == 0:
            motorR_uit()
            motorL_uit()
            grijp()
            frontlinecount = 0
            print(f'bocht={bochtcount}')
        if line_count == 2 and bochtcount == 0:
            draai_links(draaisnelheid)
            line_count = 0
            bochtcount += 1
        if line_count == 2 and bochtcount == 1:
            motorR_uit()
            motorL_uit()
            motor_running = False
        '''
        if line_count == 2 and bochtcount == 1:
            draai_rechts(snelheid)
            line_count = 0
            bochtcount += 1
            print(f'bocht={bochtcount}')

        if line_count == 2 and bochtcount == 2:
            motorR_uit()
            motorL_uit()
            grijp()
            draai_rechts(snelheid)
            line_count = 0
            bochtcount += 1
            print(f'bocht={bochtcount}')

        if line_count == 2 and bochtcount == 3:
            motorR_uit()
            motorL_uit()
            grijp()
            draai_180_graden(snelheid)
            line_count = 0
            bochtcount += 1
            print(f'bocht={bochtcount}')

        if line_count == 2 and bochtcount == 4:
            draai_links(snelheid)
            line_count = 0
            bochtcount += 1
            print(f'bocht={bochtcount}')

        if line_count == 2 and bochtcount == 5:
            motorR_uit()
            motorL_uit()
            motor_running = False


        if line_count == 1 and bochtcount == 6:
            motorR_uit()
            motorL_uit()
            grijp()
            draai_180_graden(snelheid)
            line_count = 0
            bochtcount += 1
            print(f'bocht={bochtcount}')

        if line_count == 3 and bochtcount == 7:
            draai_rechts(snelheid)
            line_count = 0
            bochtcount += 1
            print(f'bocht={bochtcount}')

        if line_count == 1 and bochtcount == 8:
            motorR_uit()
            motorL_uit()
            motor_running = False
        '''

    time.sleep(0.05)