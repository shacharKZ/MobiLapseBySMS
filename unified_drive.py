#!/usr/bin/env python
import RPi.GPIO as GPIO
import PCA9685 as p
import time    # Import necessary modules

# ===========================================================================
# Raspberry Pi pin11, 12, 13 and 15 to realize the clockwise/counterclockwise
# rotation and forward and backward movements
# ===========================================================================
Motor0_A = 11  # pin11
Motor0_B = 12  # pin12
Motor1_A = 13  # pin13
Motor1_B = 15  # pin15

# ===========================================================================
# Set channel 4 and 5 of the servo driver IC to generate PWM, thus 
# controlling the speed of the car
# ===========================================================================
# EN_M0    = 4  # servo driver IC CH4
EN_M0    = 8  # servo driver IC CH4
# EN_M1    = 5  # servo driver IC CH5
EN_M1    = 9  # servo driver IC CH5

pins = [Motor0_A, Motor0_B, Motor1_A, Motor1_B]

# ===========================================================================
# Adjust the duty cycle of the square waves output from channel 4 and 5 of
# the servo driver IC, so as to control the speed of the car.
# ===========================================================================
def setSpeed(speed):
	speed *= 40
	print(('speed is: ', speed))
	pwm.write(EN_M0, 0, speed)
	pwm.write(EN_M1, 0, speed)

def setup_motor(busnum=None):
	global forward0, forward1, backward1, backward0
	global pwm
	if busnum == None:
		pwm = p.PWM()                  # Initialize the servo controller.
	else:
		pwm = p.PWM(bus_number=busnum) # Initialize the servo controller.

	pwm.frequency = 60
	forward0 = 'True'
	forward1 = 'True'
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)        # Number GPIOs by its physical location
	try:
		for line in open("config"):
			if line[0:8] == "forward0":
				forward0 = line[11:-1]
			if line[0:8] == "forward1":
				forward1 = line[11:-1]
	except:
		pass
	if forward0 == 'True':
		backward0 = 'False'
	elif forward0 == 'False':
		backward0 = 'True'
	if forward1 == 'True':
		backward1 = 'False'
	elif forward1 == 'False':
		backward1 = 'True'
	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)   # Set all pins' mode as output

# ===========================================================================
# Control the DC motor to make it rotate clockwise, so the car will 
# move forward.
# ===========================================================================

def motor0(x):
	if x == 'True':
		GPIO.output(Motor0_A, GPIO.LOW)
		GPIO.output(Motor0_B, GPIO.HIGH)
	elif x == 'False':
		GPIO.output(Motor0_A, GPIO.HIGH)
		GPIO.output(Motor0_B, GPIO.LOW)
	else:
		print ('Config Error')

def motor1(x):
	if x == 'True':
		GPIO.output(Motor1_A, GPIO.LOW)
		GPIO.output(Motor1_B, GPIO.HIGH)
	elif x == 'False':
		GPIO.output(Motor1_A, GPIO.HIGH)
		GPIO.output(Motor1_B, GPIO.LOW)

def forward():
	motor0(forward0)
	motor1(forward1)

def backward():
	motor0(backward0)
	motor1(backward1)

def forwardWithSpeed(spd = 50):
	setSpeed(spd)
	motor0(forward0)
	motor1(forward1)

def backwardWithSpeed(spd = 50):
	setSpeed(spd)
	motor0(backward0)
	motor1(backward1)

def stop():
	for pin in pins:
		GPIO.output(pin, GPIO.LOW)

# ===========================================================================
# The first parameter(status) is to control the state of the car, to make it 
# stop or run. The parameter(direction) is to control the car's direction 
# (move forward or backward).
# ===========================================================================
def ctrl(status, direction=1):
	if status == 1:   # Run
		if direction == 1:     # Forward
			forward()
		elif direction == -1:  # Backward
			backward()
		else:
			print( 'Argument error! direction must be 1 or -1.')
	elif status == 0: # Stop
		stop()
	else:
		print ('Argument error! status must be 0 or 1.')

def test():
	while True:
		setup()
		ctrl(1)
		time.sleep(3)
		setSpeed(10)
		time.sleep(3)
		setSpeed(100)
		time.sleep(3)
		ctrl(0)

def Map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setup_direction_cont(busnum=None):
	global leftPWM, rightPWM, homePWM, pwm
	leftPWM = 400
	homePWM = 450
	rightPWM = 500
	offset =0
	try:
		for line in open('config'):
			if line[0:8] == 'offset =':
				offset = int(line[9:-1])
	except:
		print('config error')
	leftPWM += offset
	homePWM += offset
	rightPWM += offset
	if busnum == None:
		pwm = p.PWM()                  # Initialize the servo controller.
	else:
		pwm = p.PWM(bus_number=busnum) # Initialize the servo controller.
	pwm.frequency = 60
	calibrate(-60)

# ==========================================================================================
# Control the servo connected to channel 0 of the servo control board, so as to make the 
# car turn left.
# ==========================================================================================
def turn_left():
	global leftPWM
	pwm.write(0, 0, leftPWM)  # CH0

# ==========================================================================================
# Make the car turn right.
# ==========================================================================================
def turn_right():
	global rightPWM
	pwm.write(0, 0, rightPWM)

# ==========================================================================================
# Make the car turn back.
# ==========================================================================================

def turn(angle):
	angle = Map(angle, 0, 255, leftPWM, rightPWM)
	print(angle)
	pwm.write(0, 0, angle)

def home_dir():
	global homePWM
	pwm.write(0, 0, homePWM)

def calibrate(x):
	pwm.write(0, 0, 450+x)

def test():
	while True:
		turn_left()
		time.sleep(1)
		home_dir()
		time.sleep(1)
		turn_right()
		time.sleep(1)
		home_dir()

if __name__ == '__main__':
	setup_motor()
	setup_direction_cont()
	home_dir()
	time.sleep(5)
	turn_right()
	time.sleep(5)
	turn_left()
	time.sleep(5)
	home_dir()



