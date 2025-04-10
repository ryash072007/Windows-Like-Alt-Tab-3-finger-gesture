import subprocess
import pexpect
import argparse

debug = False

def start_ydotoold(root_password=None):
    global child
    command = 'sudo -b ydotoold --socket-path="$HOME/.ydotool_socket" --socket-own="$(id -u):$(id -g)"'
    child = pexpect.spawn("/bin/bash", args=["-c", command])
    child.expect("password for")
    
    if root_password is None:
        raise ValueError("Root password is required to start ydotoold.")
    
    child.sendline(root_password)
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

def run_libinput(initial_factor=0.8, threshold=30):
    try:
        process = subprocess.Popen(
            ["libinput", "debug-events"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if debug: print("libinput started successfully.")
    except subprocess.CalledProcessError as e:
        if debug: print(f"Error running fusuma: {e}")

    distance = 0
    factor = initial_factor
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
                                factor = initial_factor
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
    parser = argparse.ArgumentParser(description='Windows-like Alt-Tab 3-finger gesture')
    parser.add_argument('--password', '-p', help='Root password for ydotoold (if not provided, will prompt securely)')
    parser.add_argument('--factor', '-f', type=float, default=0.8, help='Initial sensitivity factor (default: 0.8)')
    parser.add_argument('--threshold', '-t', type=float, default=30, help='Swipe threshold distance (default: 30)')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    
    debug = args.debug
    
    start_ydotoold(args.password)
    run_libinput(args.factor, args.threshold)
    alt_up()