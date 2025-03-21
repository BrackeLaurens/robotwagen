import time
import math

# Functie om de kleur te berekenen op basis van de tijd
def calculate_rgb(t):
    L = 0.5 + 0.5 * math.sin(2 * math.pi * t)  # Kleurintensiteit volgens vergelijking (2)
    return (L, 1, L)  # RGB(kleur) volgens vergelijking (1)

# Functie om de kleur van de LED weer te geven volgens de processtap
def status_led_step(step):
    t = 0  # Begin met tijd = 0
    while True:
        if step == "beweging_naar_object":
            # Cyclus voor bewegen naar object (wit en groen)
            rgb = calculate_rgb(t)
            print(f"Beweging naar object - Kleur: RGB{rgb}")
        elif step == "verzameling_object":
            # Oranje voor objectverzameling (aan-uit cyclus)
            if int(t) % 2 == 0:
                print("Verzameling object - Kleur: Oranje")
            else:
                print("Verzameling object - Kleur: Uit")
        elif step == "achteruit_rijden":
            # Rood voor achteruit rijden (aan-uit cyclus)
            if int(t) % 2 == 0:
                print("Achteruit rijden - Kleur: Rood")
            else:
                print("Achteruit rijden - Kleur: Uit")
        elif step == "beweging_naar_garage":
            # Blauw voor beweging naar garage (constant aan)
            print("Beweging naar garage - Kleur: Blauw")

        # Wacht even voor de volgende update van de LED
        time.sleep(0.1)  # Update iedere tiende seconde
        t += 0.1  # Verhoog de tijd

# Kies een processtap en begin de loop
process_step = "beweging_naar_object"  # Verander deze waarde naar de gewenste stap
status_led_step(process_step)
