import time
import board
from analogio import AnalogIn

# Stel de analoge ingang in voor de ANALOG OUT pin van de US-100
analog_in = AnalogIn(board.GPIO1) #verander gp27 eventueel naar de juiste positie



def get_voltage(pin):
    """Bereken de spanning op de pin"""
    return (pin.value * 3.3) / 65535  # 65535 is de maximale waarde voor een 16-bits ADC


def get_distance():
    """Bereken de afstand in cm op basis van de analoge spanning"""
    voltage = get_voltage(analog_in)
    # Zet de spanning om naar afstand (0V = 0 cm, 5V = 400 cm)
    distance = (voltage / 3.3) * 400
    return distance


def check_collision():
    """Controleer of een object dichtbij is op basis van de afstand"""
    distance = get_distance()
    print("Afstand:", round(distance, 2), "cm")

    # Stel een drempelwaarde in voor botsingen
    threshold = 5  # Bijvoorbeeld 20 cm als botsingdrempel
    if distance < threshold:
        motor_stop()        #zorg voor functie motor_stop
        print("Botsing gedetecteerd!")



# Hoofdlus
while True:
    check_collision()
    time.sleep(0.1)

