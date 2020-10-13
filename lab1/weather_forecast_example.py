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

location = ''

weather_map = {
    'Thunderstorm': 50,
    'Drizzle': 50,
    'Rain': 50,
    'Snow': 50,
    'Clouds': 10,
    'Mist': 10,
    'Smoke': 10,
    'Dust': 10,
    'Haze': 10,
    'Fog': 10,
    'Ash': 10,
    'Squall': 10,
    'Tornado': 10,
    'Clear': -70
}

location_map = {
    '': 'Krakow',
    'Krakow': 'Istanbul',
    'Istanbul': 'Stockholm',
    'Stockholm': 'Istanbul'
}


def get_servo_angle(current_location):
    weather_status = owm.weather_manager().weather_at_place(current_location).weather.status
    return weather_map[weather_status]


def change_location():
    global location
    location = location_map[location]
    print("New location: " + location)


@circuit.run
def main():
    from time import sleep
    from gpiozero import AngularServo, Button

    servo1 = AngularServo(17, min_angle=-90, max_angle=90)
    button_upper = Button(12)

    change_location()
    button_upper.when_activated = change_location

    while True:
        servo1.angle = get_servo_angle(location)
        sleep(0.1)
