import time
import board
import pwmio
import adafruit_hcsr04

# Definieer de GPIO-pinnen voor de HCSR04-sensor
trigger_pin = board.GP0
echo_pin = board.GP1

# Initialiseer de HCSR04 afstandssensor
sonar = adafruit_hcsr04.HCSR04(trigger_pin, echo_pin)

# Simuleer een motor PWM-uitgang (pas pin aan indien nodig)
motor_aan_uitL = pwmio.PWMOut(board.GP2, frequency=5000, duty_cycle=65535)  # Vol vermogen

def motorL_uit():
    """ Zet de motor uit """
    motor_aan_uitL.duty_cycle = 0

def get_distance():
    """ Meet de afstand met de HCSR04 """
    try:
        return sonar.distance
    except RuntimeError:
        return None  # Indien meting mislukt

def check_collision():
    """ Controleer of een object dichtbij is en zet motor uit indien nodig """
    threshold = 5  # Botsingsdrempel in cm

    distance = get_distance()
    if distance is not None:
        print(f"Afstand: {round(distance, 2)} cm")

        if distance < threshold:
            motorL_uit()
            print("Botsing gedetecteerd! Motor uitgeschakeld!")

# Hoofdlus
while True:
    check_collision()
    time.sleep(0.1)

