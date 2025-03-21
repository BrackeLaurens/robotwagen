# Development

## Installatie

gebruik UV  (https://docs.astral.sh/uv/getting-started/installation/)

```bash
uv sync
```


```bash
pip install -r requirements.txt
```




# Hoe werkt dit?

Om dit werkend te krijgen:
1. Zorg ervoor dat je Pico en laptop op hetzelfde WiFi-netwerk zijn aangesloten
2. Zoek het IP-adres van je laptop op (gebruik ipconfig op Windows of ifconfig op Mac/Linux)
3. Werk de COMPUTER_IP in de Pico-code bij met het IP-adres van je laptop
4. Werk de WiFi-inloggegevens bij in de Pico-code
5. Start je Flask-applicatie
6. Upload en start de code op je Pico

De webpagina zal nu automatisch bijwerken wanneer deze nieuwe data ontvangt van de Pico. De data wordt elke seconde verzonden vanaf de Pico, en de webpagina werkt in realtime bij met behulp van Server-Sent Events.

Belangrijke opmerkingen:
- De UDP-poort (5005) kan worden aangepast, maar moet overeenkomen op zowel de Pico als de Flask-app
- Zorg ervoor dat je firewall inkomend UDP-verkeer toestaat op de gekozen poort
- Het voorbeeld gaat ervan uit dat de Pico tekstdata verstuurt; pas de data-verwerking aan als je andere formaten verstuurt
- Je moet mogelijk de buffergrootte (1024 bytes) aanpassen afhankelijk van je datagrootte


Door. Laurens Bracke
Op: 2/3/2025