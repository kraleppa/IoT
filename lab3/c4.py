from lab1.VirtualCopernicusNG import TkCircuit

# initialize the circuit inside the

configuration = {
    "name": "Lobby",
    "sheet": "sheet_smarthouse.png",
    "width": 332,
    "height": 300,
    "leds": [
        {"x": 112, "y": 70, "name": "LED 1", "pin": 21},
        {"x": 71, "y": 141, "name": "LED 2", "pin": 22}
    ],
    "buttons": [
        {"x": 242, "y": 146, "name": "Button 1", "pin": 11},
        {"x": 200, "y": 217, "name": "Button 2", "pin": 12},
    ]
}

circuit = TkCircuit(configuration)

@circuit.run
def main():
    # now just write the code you would use on a real Raspberry Pi

    from gpiozero import LED, Button
    import paho.mqtt.client as mqtt

    def button1_pressed():
        mqttc.publish("kraleppa/light/lobby", "TOGGLE", 0, False)

    def button2_pressed():
        mqttc.publish("kraleppa/ZONE2/light", "OFF", 0, False)

    led1 = LED(21)
    led1.off()

    button1 = Button(11)
    button2 = Button(12)

    button1.when_pressed = button1_pressed
    button2.when_pressed = button2_pressed

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        mqttc.subscribe("kraleppa/light/lobby")
        mqttc.subscribe("kraleppa/ZONE2/light")
        mqttc.publish("kraleppa/service", "Light controller c4 is working properly", 0, False)

    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        if msg.payload == b'TOGGLE':
            led1.toggle()
        elif msg.payload == b'OFF':
            led1.off()

    mqttc = mqtt.Client("kraleppa_c4")
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.will_set("kraleppa/service", payload="Light controller c4 is not working", qos=0, retain=True)


    mqttc.connect("test.mosquitto.org", 1883, 60)

    mqttc.loop_forever()