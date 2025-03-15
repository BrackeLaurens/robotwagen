import time
import board
import pwmio
import digitalio
import analogio
ldr_left = analogio.AnalogIn(board.GP27)  # LDR Links vooraan
ldr_right = analogio.AnalogIn(board.GP28)  # LDR Rechts vooraan
ldr_back = analogio.AnalogIn(board.GP26)  # LDR Achteraan

snelheid = 50

motor_aan_uitR = pwmio.PWMOut(board.GP17,frequency=1000)
motor_richtingR = digitalio.DigitalInOut(board.GP16)
motor_richtingR.direction = digitalio.Direction.OUTPUT

motor_aan_uitL = pwmio.PWMOut(board.GP18,frequency=1000)
motor_richtingL = digitalio.DigitalInOut(board.GP19)
motor_richtingL.direction = digitalio.Direction.OUTPUT

def motorR_aan(snelheid):
    duty_cycle = int((snelheid / 100) * 65535)
    motor_aan_uitR.duty_cycle = duty_cycle

def motorR_uit():
    motor_aan_uitR.duty_cycle = 0

def achteruitR():
    motor_richtingR.value=True

def vooruitR():
    motor_richtingR.value=False

def motorL_aan(snelheid):
    duty_cycle = int((snelheid / 100) * 65535)
    motor_aan_uitL.duty_cycle = duty_cycle

def motorL_uit():
    motor_aan_uitL.duty_cycle = 0

def achteruitL():
    motor_richtingL.value=True

def vooruitL():
    motor_richtingL.value=False

#defenities
DREMPEL_ZWARTE_LIJN_achter = 1.25
DREMPEL_ZWARTE_LIJN_links = 1.10
DREMPEL_ZWARTE_LIJN_rechts = 1.10
VERSCHIL_AFWIJKING_RECHTS = 0.10
VERSCHIL_AFWIJKING_LINKS = -0.10
line_count = 0

def meet_ldr(ldr):
    return ldr.value * (3.3 / 65535)  # Converteer ADC naar spanning (0 - 3.3V)

def vooruit(snelheid):
    vooruitL()
    vooruitR()
    motorR_aan(snelheid)
    motorL_aan(snelheid)

def achteruit(snelheid):
    achteruitL()
    achteruitR()
    motorR_aan(snelheid)
    motorL_aan(snelheid)

def draai_rechts(snelheid):
    while True:
        achteruitR()
        vooruitL()
        motorR_aan(snelheid)
        motorL_aan(snelheid)
        if meet_ldr(ldr_left) < DREMPEL_ZWARTE_LIJN_links and -0.20< verschil_LR <0.20:
            vooruit(snelheid)
            break
        time.sleep(0.05)


def draai_links(snelheid):
    while True:
        vooruitR()
        achteruitL()
        motorR_aan(snelheid)
        motorL_aan(snelheid)
        if meet_ldr(ldr_right) < DREMPEL_ZWARTE_LIJN_rechts and -0.20< verschil_LR <0.20:
            vooruit(snelheid)
            break
        time.sleep(0.05)


def draai_180_graden(snelheid):
    draai_links(snelheid)
    linecount_uturn = 0
    if meet_ldr(ldr_left) < DREMPEL_ZWARTE_LIJN_links:
        linecount_uturn += 1
        while meet_ldr(ldr_left) < DREMPEL_ZWARTE_LIJN_links:
            time.sleep(0.1)
    if linecount_uturn >=2 and -0.20<verschil_LR<0.20:
        vooruit(snelheid)

while True:
    vooruit(snelheid)
    licht_links = meet_ldr(ldr_left)
    licht_rechts = meet_ldr(ldr_right)
    licht_achter = meet_ldr(ldr_back)
    verschil_LR=licht_rechts-licht_links

    print(f"LDR Links: {licht_links:.2f}V | LDR Rechts: {licht_rechts:.2f}V | LDR Achter: {licht_achter:.2f}V")

    zwart_links = licht_links < DREMPEL_ZWARTE_LIJN_links
    zwart_rechts = licht_rechts < DREMPEL_ZWARTE_LIJN_rechts
    zwart_achter = licht_achter < DREMPEL_ZWARTE_LIJN_achter
    
    if zwart_achter:
        print("Zwarte lijn achteraan voorbij")
        line_count += 1
        while meet_ldr(ldr_back) < DREMPEL_ZWARTE_LIJN_achter: #wachten met counten tot zwarte lijn voorbij is.
            time.sleep(0.1)
    
    # Voorste LDR’s sturen bij zodat auto zwarte lijn volgt.
    if -0.20<verschil_LR < 0.20:  #als het verschil tussen de 2 ldr's niet groot is, zit hij op de lijn.
        vooruit(snelheid)

    elif zwart_links: #afwijking naar rechts
        motorR_aan(snelheid + 10)
        motorL_aan(snelheid - 10)

    elif zwart_rechts: #afwijking naar links
        motorR_aan(snelheid - 10)
        motorL_aan(snelheid + 10)

    else:
        vooruit(snelheid)
    time.sleep(0.1)