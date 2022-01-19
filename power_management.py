import subprocess


def check_voltage():
    print(f'-----------------------------------')
    temp_res = subprocess.getstatusoutput(f'vcgencmd measure_volts core')
    print(temp_res)
    temp_res = subprocess.getstatusoutput(f'vcgencmd get_throttled')
    print(temp_res)
    print(f'-----------------------------------\n')


if __name__ == '__main__':
    import time

    for i in range(121):
        check_voltage()
        time.sleep(1)
