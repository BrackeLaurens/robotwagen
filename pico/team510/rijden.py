# Write your code here :-)
#Besturingsalgoritme zelfrijdende robotwagen

import time
import board
import pwmio
import digitalio
import analogio
ldr_right = analogio.AnalogIn(board.GP28)  # ldr rechts vooraan
ldr_left = analogio.AnalogIn(board.GP27)  # ldr links vooraan
ldr_back = analogio.AnalogIn(board.GP26)  # ldr Achteraan

snelheid = 50 #snelheid voor alle maneuvers tijdens de uitvoering, kan later aangepast worden.
bochtcount = 0
line_count = 0
rijden_actief = False

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
    rijden_actief = False

def achteruitR():
    motor_richtingR.value=True

def vooruitR():
    motor_richtingR.value=False

def motorL_aan(snelheid):
    duty_cycle = int((snelheid / 100) * 65535)
    motor_aan_uitL.duty_cycle = duty_cycle

def motorL_uit():
    motor_aan_uitL.duty_cycle = 0
    rijden_actief = False

def achteruitL():
    motor_richtingL.value=True

def vooruitL():
    motor_richtingL.value=False

#defenities
DREMPEL_ZWARTE_LIJN_achter = 1.25
DREMPEL_ZWARTE_LIJN_links = 1.45
DREMPEL_ZWARTE_LIJN_rechts = 1.45


def meet_ldr(ldr):
    return ldr.value * (3.3 / 65535)  # Converteren naar spanning in Volt (0 - 3.3V)

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
    achteruitR()
    vooruitL()
    motorR_aan(snelheid)
    motorL_aan(snelheid)

    while meet_ldr(ldr_right) > DREMPEL_ZWARTE_LIJN_rechts:
        print(meet_ldr(ldr_right))
        time.sleep(0.1)

def draai_links(snelheid):
    achteruitL()
    vooruitR()
    motorR_aan(snelheid)
    motorL_aan(snelheid)

    while meet_ldr(ldr_left) > DREMPEL_ZWARTE_LIJN_links:
        #print(meet_ldr(ldr_left))
        time.sleep(0.1)


def draai_180_graden(snelheid):
    achteruitL()
    vooruitR()
    motorR_aan(snelheid)
    motorL_aan(snelheid)

    linecount_uturn = 0
    while linecount_uturn < 2:
        if meet_ldr(ldr_left) <= DREMPEL_ZWARTE_LIJN_links:
            linecount_uturn += 1
            while meet_ldr(ldr_left) <= DREMPEL_ZWARTE_LIJN_links:
                time.sleep(0.05)
        time.sleep(0.05)
    vooruit(snelheid)


def go():
    rijden_actief = True


while rijden_actief:
    vooruit(snelheid)
    verschil_LR = meet_ldr(ldr_left) - meet_ldr(ldr_right)
    #printen van de voltages van de 3 ldr's om betere testen uit te voeren.
    #print(f"LDR Links: {meet_ldr(ldr_left):.2f}V | LDR Rechts: {meet_ldr(ldr_right):.2f}V | LDR Achter: {meet_ldr(ldr_back):.2f}V")

    zwart_links = meet_ldr(ldr_left) < DREMPEL_ZWARTE_LIJN_links
    zwart_rechts = meet_ldr(ldr_right) < DREMPEL_ZWARTE_LIJN_rechts
    zwart_achter = meet_ldr(ldr_back) < DREMPEL_ZWARTE_LIJN_achter

    if zwart_achter: #linecounter voor achterste ldr (om te weten wanneer er moet gedraaid worden)
        line_count += 1
        print(line_count)
        while meet_ldr(ldr_back) < DREMPEL_ZWARTE_LIJN_achter: #wachten met counten tot zwarte lijn voorbij is.
            time.sleep(0.1)

    # Voorste LDR’s sturen bij zodat auto zwarte lijn volgt.
    if -0.20<verschil_LR < 0.20:  #als het verschil tussen de 2 ldr's niet groot is, zit hij op de lijn.
        vooruit(snelheid)

    elif zwart_links: #afwijking naar rechts (linkse ldr komt over zwarte lijn)
        motorR_aan(snelheid + 10)
        motorL_aan(snelheid - 10)

    elif zwart_rechts: #afwijking naar links (rechtse ldr komt over zwarte lijn)
        motorR_aan(snelheid - 10)
        motorL_aan(snelheid + 10)

    else: #er is niks aan de hand, auto moet gewoon vooruit rijden.
        vooruit(snelheid)
    time.sleep(0.1)

    if line_count == 2 and bochtcount !=3:
        draai_links(snelheid)
        line_count = 0
        bochtcount += 1
        print(f'bocht={bochtcount}')
    if line_count == 2 and bochtcount ==3:
        motorR_uit()
        motorL_uit()
        print("einde")
        break
    '''
    if line_count == 2:
        draai_180_graden(snelheid)
        line_count = 0
    '''

