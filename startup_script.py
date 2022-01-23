import requests
import subprocess
import time
import video_dir as vid


if __name__ == '__main__':
    vid.setup_vid()
    time.sleep(5)
    for i in range(10):
        try:
            request = requests.get("http://www.google.com", timeout=7)
            print("Connected to the Internet! let's rock!")
            vid.home_x_y()
            vid.move_increase_y()
            time.sleep(0.2)
            vid.move_increase_y()
            time.sleep(0.5)
            vid.move_decrease_y()
            time.sleep(0.2)
            vid.move_decrease_y()
            subprocess.call("python3 app.py", shell=True)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            exit()
        except (requests.ConnectionError, requests.Timeout) as exception:
            print("No internet connection yet...")
            vid.make_gesture(1)

        time.sleep(10)
