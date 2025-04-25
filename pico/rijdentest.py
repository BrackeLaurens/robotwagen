# Write your code here :-)
# Besturingsalgoritme zelfrijdende robotwagen

import time
import board
import pwmio
import digitalio
import math
import analogio
from adafruit_motor import servo

rijden_actief = False

def go():
    global rijden_actief
    rijden_actief = True  # lol
    assert rijden_actief == True, 'rijden_actief moet True zijn'
    print('yellah')

def motorR_uit():
    global rijden_actief
    print("[DEBUG] Rechts motor UIT aangevraagd")  # Debug print

    rijden_actief = False

    print('motorR is uit')
    assert rijden_actief == False, 'rijden actief moet false zijn'


def motorL_uit():
    global rijden_actief
    print("[DEBUG] Links motor UIT aangevraagd")  # Debug print

    rijden_actief = False

    print('motorL is uit')
    assert rijden_actief == False, 'rijden actief moet false zijn'







