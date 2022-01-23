import subprocess
import time

from db_handler import write_robot_warning_to_db

threshold_const_msg = 84
last_voltage_len = 100
# True = detected a low voltage at the moment, False = did not detected a low voltage at the moment
last_volt_results = [False] * last_voltage_len
time_between_checking = 0.5
last_time_check = 0
time_between_alerting = 25
last_time_alert_voltage = 0
last_time_alert_heat = 0


def setup_power_management():
    global threshold_const_msg, last_voltage_len, last_volt_results, time_between_checking, last_time_check, time_between_alerting, last_time_alert_voltage, last_time_alert_heat
    threshold_const_msg = 84
    last_voltage_len = 100
    last_volt_results = [False] * last_voltage_len
    time_between_checking = 0.5
    last_time_check = 0
    time_between_alerting = 25
    last_time_alert_voltage = 0
    last_time_alert_heat = 0


def check_voltage():
    global threshold_const_msg, last_voltage_len, last_volt_results, time_between_checking, last_time_check, time_between_alerting, last_time_alert_voltage, last_time_alert_heat
    current_time = time.time()
    if current_time - last_time_check < time_between_checking:
        return  # not enough time between two checks
    temp_res = subprocess.getstatusoutput(f'vcgencmd get_throttled')
    print(temp_res)  # for debugging
    # # TODO consider to just check the last number instead
    error_code_str = temp_res[1][12:]  # only the throttled's code
    # print("error_code is: ", error_code_str)
    # if not error_code_str.isnumeric:
    #     print("Faild to check power management. This module might not work or return false data!")
    #     return

    # error_code_num = int(error_code_str)
    del last_volt_results[0]
    last_volt_results.append(error_code_str == '50005')
    # last_volt_results.append(error_code_num % 2 != 0)  # if we choose to use numeric
    last_time_check = current_time
    if last_volt_results.count(True) > threshold_const_msg and current_time - last_time_alert_voltage > time_between_alerting:
        write_robot_warning_to_db(
            'Robot battery is low, robot will shut down and battery might be damaged if not recharged soon.')
        print(f'detect low voltage!!!! VV ^^ VV ^^')

    print(f'debug power management: ', last_volt_results)
    print(f'statics={last_volt_results.count(True)}/{last_voltage_len} ---> {last_volt_results.count(True)/last_voltage_len}')

    temp_res2 = subprocess.getstatusoutput(f'vcgencmd measure_temp')
    print(temp_res2)  # for debugging
    board_temp = float(temp_res2[1][5:-2])
    print(f'board temperature is {board_temp}')
    if board_temp >= 55 and current_time - last_time_alert_heat > time_between_alerting:  # TODO set threshold
        write_robot_warning_to_db(
            'Robot temperature is very high, consider stopping the robot and letting it cool.')
        print(
            f'Board overheat! its current temperature is {board_temp}, maybe you should stop it!!!!')


if __name__ == '__main__':

    setup_power_management()

    for i in range(5555):
        check_voltage()
        time.sleep(0.2)
