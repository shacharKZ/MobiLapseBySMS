#!/usr/bin/env python
import PCA9685 as servo
import time                # Import necessary modules


TURN_15, TURN_25, TURN_35, TURN_45, TURN_60 = 20, 30, 42, 55, 72
pwm = servo.PWM() 

def Map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setup_direction(busnum=None):
	global leftPWM, rightPWM, homePWM, pwm
	global left_15, left_30, left_45, right_15, right_30, right_45
	print("setting up dir: ", end="")
	leftPWM = 400
	homePWM = 450
	rightPWM = 500
	offset =0  # the offest is taken from the gile "config" (line 3 is the offest we looking for)
	try:
		for line in open('config'):
			if line[0:8] == 'offset =':
				offset = int(line[9:-1])
	except:
		print('config error')
	print(f'offset is: {offset}')
	leftPWM += offset
	homePWM += offset
	rightPWM += offset
	if busnum == None:
		pwm = servo.PWM()                  # Initialize the servo controller.
	else:
		pwm = servo.PWM(bus_number=busnum) # Initialize the servo controller.
	pwm.frequency = 60
	calibrate(-60)

# ==========================================================================================
# Control the servo connected to channel 0 of the servo control board, so as to make the 
# car turn left.
# ==========================================================================================
def turn_left():
	global leftPWM
	pwm.write(0, 0, leftPWM)  # CH0

def turn_left(added_angle = 0):
	global homePWM, pwm
	pwm.write(0, 0, homePWM-added_angle) 

# ==========================================================================================
# Make the car turn right.
# ==========================================================================================
def turn_right():
	global rightPWM
	pwm.write(0, 0, rightPWM)

def turn_right(add_angle = 0):
	global homePWM, pwm
	pwm.write(0, 0, homePWM + add_angle)

# ==========================================================================================
# Make the car turn back.
# ==========================================================================================

def turn(angle):
	angle = Map(angle, 0, 255, leftPWM, rightPWM)
	pwm.write(0, 0, angle)

def home(dummy_param = None):
	global homePWM, pwm
	pwm.write(0, 0, homePWM)

def calibrate(x):
	pwm.write(0, 0, 450+x)

def test():
	while True:
		turn_left()
		time.sleep(1)
		home()
		time.sleep(1)
		turn_right()
		time.sleep(1)
		home()

def test2():
	setup_direction()
	home()
	time.sleep(1.5)
	for a in [TURN_15, TURN_25, TURN_35, TURN_45, TURN_60]:
		turn_left(a)
		time.sleep(1.5)
	
	for a in [TURN_15, TURN_25, TURN_35, TURN_45, TURN_60]:
		turn_right(a)
		time.sleep(1.5)
	
	# turn_left(TURN_15)
	# time.sleep(1.5)
	# turn_right()
	# time.sleep(1.5)
	home()

if __name__ == '__main__':
	setup_direction()
	test2()

	# for i in range(homePWM, leftPWM-100, -10):
	# 	print(i)
	# 	time.sleep(1)
	print("done")

