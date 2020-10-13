from VirtualCopernicusNG import TkCircuit
import pyowm
from lab1.api_key import key

# initialize the circuit inside the

configuration = {
    "name": "CopernicusNG Weather Forecast",
    "sheet": "sheet_forecast.png",
    "width": 343,
    "height": 267,

    "servos": [
        {"x": 170, "y": 150, "length": 90, "name": "Servo 1", "pin": 17}
    ],
    "buttons": [
        {"x": 295, "y": 200, "name": "Button 1", "pin": 11},
        {"x": 295, "y": 170, "name": "Button 2", "pin": 12},
    ]
}

circuit = TkCircuit(configuration)
owm = pyowm.OWM(key)

location = "Krakow"


def get_servo_angle(location):
    weather_status = owm.weather_manager().weather_at_place(location).weather.status
    print(weather_status)
    if weather_status == "Clear":
        return -70
    elif weather_status == "Few clouds":
        return -30
    elif weather_status == "Clouds":
        return 10
    elif weather_status == "Rain":
        return 50


def change_location():
    global location
    if location == "Krakow":
        location = "Istanbul"
    elif location == "Istanbul":
        location = "Stockholm"
    elif location == "Stockholm":
        location = "Istanbul"
    print(location)


@circuit.run
def main():
    from time import sleep
    from gpiozero import AngularServo, Button

    servo1 = AngularServo(17, min_angle=-90, max_angle=90)
    button_upper = Button(12)

    button_upper.when_activated = change_location

    while True:
        for x in range(-90, 70):
            servo1.angle = get_servo_angle(location)
            sleep(0.1)
