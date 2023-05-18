from led import Led
from servo import Servo

led = Led(0, 10000)
servo = Servo(15, 50)

def wait_for_input():
    readback = input()

    string_params = readback.split(" ")

    if len(string_params) == 2:
        try:
            params = [int(i) for i in string_params]
        except ValueError:
            print("Wrong type params given. Need ints. Restarting...")
            return None

        return move_devices(*params)

    print(
        "incorrect number of params given. Need 2 (brightness, angle). Restarting..."
    )
    return None

def move_devices(led_value: int, servo_value: int):
    led.drive(led_value)
    servo.drive(servo_value)

while True:
    wait_for_input()
