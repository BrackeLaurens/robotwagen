import time
import board
import pwmio
import math

# Definieer de pins voor de RGB LED
RED_PIN = board.GP7
GREEN_PIN = board.GP8
BLUE_PIN = board.GP9

# Maak PWM-uitgangen voor elke kleur
red = pwmio.PWMOut(RED_PIN, frequency=1000, duty_cycle=0)
green = pwmio.PWMOut(GREEN_PIN, frequency=1000, duty_cycle=0)
blue = pwmio.PWMOut(BLUE_PIN, frequency=1000, duty_cycle=0)

# Functie om de LED-kleur in te stellen (waarden tussen 0 en 65535)
def set_color(r, g, b):
    red.duty_cycle = r
    green.duty_cycle = g
    blue.duty_cycle = b

# Functie voor het berekenen van de L(t) waarde op basis van de tijd
def L(t):
    return int((0.5 + 0.5 * math.sin(2 * math.pi * t)) * 65535)

# Hoofdlus voor het doorlopen van de processtappen
t = 0
while True:
    # 1. Beweging naar het volgende object: Wit en groen, cyclus volgens L(t)
    for i in range(100):  # Itereer over de tijd
        brightness = L(i / 10)  # Verander de helderheid met L(t)
        set_color(brightness, 65535, brightness)  # Wit en groen
        time.sleep(0.1)

    # 2. Verzameling object: Oranje, aan-uit cyclus
    for i in range(5):  # Aan-uit cyclus voor oranje
        set_color(65535, 32767, 0)  # Oranje
        time.sleep(0.5)  # Wacht 0.5 seconden
        set_color(0, 0, 0)  # LED uit
        time.sleep(0.5)  # Wacht 0.5 seconden

    # 3. Achteruit rijden: Rood, aan-uit cyclus
    for i in range(5):  # Herhaal de aan-uit cyclus 5 keer voor knipperen
        set_color(65535, 0, 0)  # Zet de LED op rood
        time.sleep(0.5)  # LED blijft 0.5 seconden aan
        set_color(0, 0, 0)  # Zet de LED uit
        time.sleep(0.5)  # LED blijft 0.5 seconden uit

    # 4. Beweging naar garage: Blauw, constant aan
    set_color(0, 0, 65535)  # Blauw, constant aan
    time.sleep(10)  # Laat de blauwe LED 10 seconden branden

    # Herhaal het proces door de hoofdlus opnieuw te starten
    # De tijd tussen herhalingen kan worden toegevoegd indien nodig
    # time.sleep(1)  # Pauze voor herstart van de loop
# Write your code here :-)
