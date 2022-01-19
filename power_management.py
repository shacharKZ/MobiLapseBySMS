import subprocess
import time

const_under_voltage_msgs = 0  # TODO not usebale. remove later
threshold_const_msg = 14
last_voltage_len = 20
# True = detected a low voltage at the moment, False = did not detected a low voltage at the moment
last_volt_results = [False] * last_voltage_len
time_between_checking = 1
last_time_check = 0


def setup_power_management():
    global const_under_voltage_msgs, threshold_const_msg, last_voltage_len, last_volt_results, time_between_checking, last_time_check
    const_under_voltage_msgs = 0
    threshold_const_msg = 14
    last_voltage_len = 20
    last_volt_results = [False] * last_voltage_len
    time_between_checking = 1
    last_time_check = 0


def check_voltage():
    global const_under_voltage_msgs, threshold_const_msg, last_voltage_len, last_volt_results, time_between_checking, last_time_check
    current_time = time.time()
    if current_time - last_time_check < time_between_checking:
        return  # not enough time between two checks
    temp_res = subprocess.getstatusoutput(f'vcgencmd get_throttled')
    print(temp_res)  # for debugging
    # TODO consider to just check the last number instead
    error_code_str = temp_res[1][12:]  # only the throttled's code
    print("error_code is: ", error_code_str)
    if not error_code_str.isnumeric:
        print("Faild to check power management. This module might not work or return false data!")
        return

    error_code_num = int(error_code_str)
    del last_volt_results[0]
    last_volt_results.append(error_code_num % 2 != 0)
    last_time_check = current_time
    if last_volt_results.count(True) > threshold_const_msg:
        # TODO send app msg "LOW VOLTAGE..."
        print(f'detect low voltage!!!! VV ^^ VV ^^')
    print(f'debug power management: ', last_volt_results)


# def check_voltage():
#     global const_under_voltage_msgs, threshold_const_msg
#     print(f'-----------------------------------')
#     # temp_res = subprocess.getstatusoutput(f'vcgencmd measure_volts core')
#     # print(temp_res)
#     temp_res = subprocess.getstatusoutput(f'vcgencmd get_throttled')
#     print(temp_res)  # for debugging
#     error_code_str = temp_res[1][12:]  # only the throttled's code
#     print("error_code is: ", error_code_str)
#     if not error_code_str.isnumeric:
#         print("Faild to check power management. This module might not work or return false data!")
#         return False
#     error_code_num = int(error_code_str)
#     if error_code_num % 2 == 0:
#         const_under_voltage_msgs = 0
#     else:
#         const_under_voltage_msgs += 1
#         if const_under_voltage_msgs > threshold_const_msg:
#             return False
#     return True

if __name__ == '__main__':

    setup_power_management()

    for i in range(121):
        check_voltage()
        time.sleep(1)
