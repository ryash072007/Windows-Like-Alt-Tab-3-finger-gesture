import subprocess
import pexpect
from dotenv import load_dotenv
import os


load_dotenv()

debug = False

def start_ydotoold():
    global child
    command = 'sudo -b ydotoold --socket-path="$HOME/.ydotool_socket" --socket-own="$(id -u):$(id -g)"'
    child = pexpect.spawn("/bin/bash", args=["-c", command])
    child.expect("password for")
    child.sendline(os.getenv("root_password"))
    child.expect(pexpect.EOF)
    if debug: print(child.before.decode("utf-8"))


def alt_down():
    subprocess.run(
        'YDOTOOL_SOCKET="$HOME/.ydotool_socket" ydotool key 56:1;',
        shell=True,
    )


def alt_up():
    subprocess.run(
        ['YDOTOOL_SOCKET="$HOME/.ydotool_socket" ydotool key 56:0;'],
        shell=True,
    )

def tab():
    subprocess.run(
        'YDOTOOL_SOCKET="$HOME/.ydotool_socket" ydotool key 15:1;',
        shell=True,
    )
    subprocess.run(
        'YDOTOOL_SOCKET="$HOME/.ydotool_socket" ydotool key 15:0;',
        shell=True,
    )

def shift_tab():
    subprocess.run(
        'YDOTOOL_SOCKET="$HOME/.ydotool_socket" ydotool key 42:1;',
        shell=True,
    )
    tab()
    subprocess.run(
        'YDOTOOL_SOCKET="$HOME/.ydotool_socket" ydotool key 42:0;',
        shell=True,
    )

def run_libinput():
    try:
        process = subprocess.Popen(
            ["libinput", "debug-events"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if debug: print("libinput started successfully.")
    except subprocess.CalledProcessError as e:
        if debug: print(f"Error running fusuma: {e}")

    distance = 0
    factor = 0.8
    threshold = 30
    while True:
        try:
            output = process.stdout.readline()
            if output == b"" and process.poll() is not None:
                break
            if output:
                output = output.decode("utf-8")
                if "GESTURE_SWIPE_" in output:
                    data = output.split()
                    del data[0]
                    if data[0] == "GESTURE_SWIPE_UPDATE":
                        del data[1]
                        del data[4:]
                        data[-1] = data[-1][:data[-1].find("/")]
                        if data[1].isdigit():
                            del data[:]
                    if data and data[2] == "3":
                        match data[0]:
                            case "GESTURE_SWIPE_BEGIN":
                                if debug: print("Gesture started.")
                                distance = 0
                                factor = 1
                                alt_down()
                            case "GESTURE_SWIPE_END":
                                if debug: print("Gesture ended.")
                                alt_up()
                            case "GESTURE_SWIPE_UPDATE":
                                distance += float(data[3]) * factor
                                if debug: print(
                                    f"Distance: {distance:.2f}"
                                )
                                if distance > threshold:
                                    distance = 0
                                    factor *= 0.7
                                    if debug: print("right")
                                    tab()
                                if distance < -threshold:
                                    distance = 0
                                    factor *= 0.7
                                    if debug: print("left")
                                    shift_tab()
                            case _:
                                pass
        except KeyboardInterrupt:
            print("Keyboard interrupt received. Stopping libinput.")
            process.terminate()
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break


if __name__ == "__main__":
    start_ydotoold()
    run_libinput()
    alt_up()                                                                                                                                                                                                                                                                                                                                
