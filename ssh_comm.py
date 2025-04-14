import paramiko
from time import sleep


client = paramiko.SSHClient()

def set_ssh_connection():
    '''
    Set-up SSH client and connect to Raspberry Pi
    '''

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # connect to Raspberry Pi
    # enter your IP address of RapsPi -> 'xxx.xxx.xxx.xxx',
    # your user name -> 'your_user_name'
    # and your password -> 'your_password'
    client.connect('xxx.xxx.xxx.xxx', username = 'your_user_name', password = 'your_password')


def close_ssh_connection():
    '''
    Close ssh connection
    '''

    client.close()


def gesture_commands(sign_command: str):
    '''
    List of gesture commands to be sent via ssh to RaspPi 4
    '''

    command = sign_command.capitalize()

    try:
        print(f"Gesture command is: {command}")

        # enter your path to file on RapsPi -> path_to_file
        if command == "One":
            client.exec_command('python3 /home/path_to_file/gest_LED_control.py One')
            sleep(1.5)
            client.exec_command('pkill python3')
            #sleep(1)
        elif command == "Two":
            client.exec_command('python3 /home/path_to_file/gest_LED_control.py Two')
            sleep(1.5)
            client.exec_command('pkill python3')
            #sleep(1)
        elif command == "Three":
            client.exec_command('python3 /home/path_to_file/gest_LED_control.py Three')
            sleep(1.5)
            client.exec_command('pkill python3')
            #sleep(1)
        elif command == "Four":
            client.exec_command('python3 /home/path_to_file/gest_LED_control.py Four')
            sleep(1.5)
            client.exec_command('pkill python3')
            #sleep(1)
        elif command == "Five":
            client.exec_command('python3 /home/path_to_file/gest_LED_control.py Five')
            sleep(1.5)
            client.exec_command('pkill python3')
            #sleep(1)
        elif command == "Thumb":
            client.exec_command('python3 /home/path_to_file/gest_LED_control.py Thumb')
            sleep(1.5)
            client.exec_command('pkill python3')
            #sleep(1)
        elif command == "OK":
            client.exec_command('python3 /home/path_to_file/gest_LED_control.py OK')
            sleep(1.5)
            client.exec_command('pkill python3')
            #sleep(1)
        elif command == "Call_me":
            client.exec_command('python3 /home/path_to_file/gest_LED_control.py Call_me')
            sleep(1.5)
            client.exec_command('pkill python3')
            #sleep(1)
        elif command == "Trident":
            client.exec_command('python3 /home/path_to_file/gest_LED_control.py Trident')
            sleep(1.5)
            client.exec_command('pkill python3')
            #sleep(1)
        elif command == "Pitch_black":
            client.exec_command('python3 /home/path_to_file/gest_LED_control.py Pitch_black')
            sleep(1.5)
            client.exec_command('pkill python3')
            #sleep(1)
        elif command == "Quit":
            client.exec_command('python3 /home/path_to_file/gest_LED_control.py Quit')
            sleep(1.5)
            client.exec_command('pkill python3')
            #sleep(1)
        else:
            print("Unknown command")

    except KeyboardInterrupt:
        print("User's Ctrl+C detected.")
        # enter your path to file on RapsPi -> path_to_file
        client.exec_command('python3 /home/path_to_file/gest_LED_control.py Quit')

    finally:
        # kill the process
        client.exec_command('pkill python3')



# to check if the commands works properly
# then import the script into "gestures_recognition.py"

# commands = ['One', 'Two', 'Three', 'Four', 'Five', 'Thumb', 'OK',
#              'Call_me', 'Trident', 'Pitch_black', 'Quit']
# for command in commands:
#     sleep(1.5)
#     print(f"Function command: {command}")
#     gesture_commands(command)

# set_ssh_connection()
# gesture_commands(sign_command="Call_me")
# gesture_commands(sign_command="Quit")
# close_ssh_connection()
