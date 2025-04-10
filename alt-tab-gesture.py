import subprocess
import pexpect
from dotenv import load_dotenv
import os


load_dotenv()


def start_ydotoold():
    global child
    command = 'sudo -b ydotoold --socket-path="$HOME/.ydotool_socket" --socket-own="$(id -u):$(id -g)"'
    child = pexpect.spawn("/bin/bash", args=["-c", command])
    child.expect("password for")
    child.sendline(os.getenv("root_password"))
    child.expect(pexpect.EOF)
    print(child.before.decode("utf-8"))


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
        print("libinput started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running fusuma: {e}")

    init_time = 0
    velocity = 0
    distance = 0
    while True:
        try:
            output = process.stdout.readline()
            if output == b"" and process.poll() is not None:
                break
            if output:
                output = output.decode("utf-8")
                if "GESTURE_SWIPE_" in output:
                    # print(output)
                    data = output.split()
                    del data[0]
                    if data[0] == "GESTURE_SWIPE_UPDATE":
                        del data[1]
                        del data[4:]
                        data[-1] = data[-1][:data[-1].find("/")]
                        if data[1].isdigit():
                            del data[:]
                    if data:
                        match data[0]:
                            case "GESTURE_SWIPE_BEGIN":
                                print("Gesture started.")
                                init_time = float(data[1].strip("+s"))
                                velocity = 0
                                distance = 0
                                alt_down()
                            case "GESTURE_SWIPE_END":
                                print("Gesture ended.")
                                alt_up()
                            case "GESTURE_SWIPE_UPDATE":
                                current_time = float(data[1].strip("+s"))
                                time_spent = (current_time - init_time)
                                distance += velocity * time_spent + 0.5 * float(data[3]) * time_spent**2
                                velocity += float(data[3]) * time_spent
                                init_time = current_time
                                print(
                                    f"Distance: {distance:.2f}, Velocity: {velocity:.2f}"
                                )
                                if distance > 0.1:
                                    print("right")
                                    tab()
                                    velocity = 0
                                    distance = 0
                                if distance < -0.1:
                                    print("left")
                                    shift_tab()
                                    velocity = 0
                                    distance = 0
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
