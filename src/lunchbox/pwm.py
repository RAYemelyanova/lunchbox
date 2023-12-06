"""Demonstrates how to control the laser and servo with PWM"""
import pigpio

SERVO_CHANNEL = 18
LED_CHANNEL = 19

pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("Cannot connect pi to pigpio")

def control_servo(pulsewidth):
    """Send a signal to make the servo move. Pulsewidth can be between 500 and 2500."""
    pi.set_servo_pulsewidth(SERVO_CHANNEL, pulsewidth)

def control_led(frequency, pwm):
    """Set the LED to a brightness, between 0-100, for a given frequency."""
    pi.set_PWM_frequency(LED_CHANNEL, frequency)
    pi.set_PWM_dutycycle(LED_CHANNEL, pwm)

