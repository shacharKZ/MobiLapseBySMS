import subprocess


def check_voltage():
    temp_res = subprocess.getstatusoutput(f'vcgencmd measure_volts core')
    print(temp_res)
    temp_res = subprocess.getstatusoutput(f'vcgencmd get_throttled')
    print(temp_res)
    print(temp_res[-1])
    print(temp_res[-4])


if __name__ == '__main__':
    import time

    for i in range(120):
        print(f'--------------- {i} ---------------')
        check_voltage()
        time.sleep(1.5)
