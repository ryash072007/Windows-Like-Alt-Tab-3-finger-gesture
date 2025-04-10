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


def run_fusuma():
    try:
        process = subprocess.Popen(
            ["fusuma", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print("Fusuma started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running fusuma: {e}")

    while True:
        try:
            output = process.stdout.readline()
            if output == b"" and process.poll() is not None:
                break
            if output:
                output = output.decode("utf-8")
                if "GESTURE_SWIPE_" in output:
                    record_start = output.find("GESTURE_SWIPE_")
                    output = output[record_start:].split("\t")
                    gesture_finger_count = output[1][0]

                    if gesture_finger_count == "3":
                        gesture_type = output[0].split(" ")[0]
                        match gesture_type:
                            case "GESTURE_SWIPE_BEGIN":
                                alt_down()
                            case "GESTURE_SWIPE_END":
                                alt_up()
                            case "GESTURE_SWIPE_UPDATE":
                                print(output[1][2:7])
                                subprocess.run(
                                    [
                                        'YDOTOOL_SOCKET="$HOME/.ydotool_socket" ydotool key 15:1 15:0;'
                                    ],
                                    shell=True,
                                )
                            case _:
                                print(f"Unknown gesture type: {gesture_type}")
        except KeyboardInterrupt:
            print("Keyboard interrupt received. Stopping fusuma.")
            process.terminate()
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break


if __name__ == "__main__":
    start_ydotoold()
    run_fusuma()
    alt_up()                                                                                                                                                                                                                                                                                                                                
