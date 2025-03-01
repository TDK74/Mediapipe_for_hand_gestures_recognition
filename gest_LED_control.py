import RPi.GPIO as GPIO
import time
import argparse


LED1 = 10
LED2 = 12
LED3 = 16
LED4 = 18
LED5 = 22

def set_up_LEDs():
    '''
    Set-up GPIO channels for LEDs control
    '''

    GPIO.setmode(GPIO.BOARD)
    GPIO.cleanup()
    GPIO.setup(LED1, GPIO.OUT)
    GPIO.setup(LED2, GPIO.OUT)
    GPIO.setup(LED3, GPIO.OUT)
    GPIO.setup(LED4, GPIO.OUT)
    GPIO.setup(LED5, GPIO.OUT)


#  Set up argparse for receiving args from command line
parser = argparse.ArgumentParser(description="Control LED on Raspberry Pi")
parser.add_argument('gesture_command', type=str, help="command for LEDs control")
args = parser.parse_args()
command = args.gesture_command

set_up_LEDs()
#time.sleep(1)

try:
    print("Waiting for commands. Ctrl+C to exit manually.")

    while True:

            if command == 'One':
                GPIO.output(LED1, 1)
                GPIO.output(LED2, 0)
                GPIO.output(LED3, 0)
                GPIO.output(LED4, 0)
                GPIO.output(LED5, 0)

            elif command == 'Two':
                GPIO.output(LED1, 1)
                GPIO.output(LED2, 1)
                GPIO.output(LED3, 0)
                GPIO.output(LED4, 0)
                GPIO.output(LED5, 0)

            elif command == 'Three':
                GPIO.output(LED1, 1)
                GPIO.output(LED2, 1)
                GPIO.output(LED3, 1)
                GPIO.output(LED4, 0)
                GPIO.output(LED5, 0)

            elif command == 'Four':
                GPIO.output(LED1, 1)
                GPIO.output(LED2, 1)
                GPIO.output(LED3, 1)
                GPIO.output(LED4, 1)
                GPIO.output(LED5, 0)

            elif command == 'Five':
                GPIO.output(LED1, 1)
                GPIO.output(LED2, 1)
                GPIO.output(LED3, 1)
                GPIO.output(LED4, 1)
                GPIO.output(LED5, 1)

            elif command == 'Thumb':
                GPIO.output(LED1, 0)
                GPIO.output(LED2, 0)
                GPIO.output(LED3, 0)
                GPIO.output(LED4, 0)
                GPIO.output(LED5, 1)

            elif command == 'OK':
                GPIO.output(LED1, 0)
                GPIO.output(LED2, 0)
                GPIO.output(LED3, 1)
                GPIO.output(LED4, 1)
                GPIO.output(LED5, 1)

            elif command == 'Call_me':
                GPIO.output(LED1, 1)
                GPIO.output(LED2, 0)
                GPIO.output(LED3, 0)
                GPIO.output(LED4, 0)
                GPIO.output(LED5, 1)

            elif command == 'Trident':
                GPIO.output(LED1, 0)
                GPIO.output(LED2, 1)
                GPIO.output(LED3, 1)
                GPIO.output(LED4, 1)
                GPIO.output(LED5, 0)

            elif command == 'Pitch_black':
                GPIO.output(LED1, 0)
                GPIO.output(LED2, 0)
                GPIO.output(LED3, 0)
                GPIO.output(LED4, 0)
                GPIO.output(LED5, 0)

            elif command == 'Quit':
                break

            else:
                print('Unknown command!')

except KeyboardInterrupt:
    print("User's Ctrl+C detected.")

finally:
    GPIO.cleanup()
