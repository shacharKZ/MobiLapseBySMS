import wiringpi as wp
import RPi.GPIO as GPIO
import time

PIN = 18  # 5
PWMA1 = 6  # gnd
PWMA2 = 13  # 2
PWMB1 = 20  # gnd
PWMB2 = 21  # miso
D1 = 12  # 1
D2 = 26  # ce1
ECHO = 4
TRIG = 14

PWM = 25

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(PWMA1, GPIO.OUT)
GPIO.setup(PWMA2, GPIO.OUT)
GPIO.setup(PWMB1, GPIO.OUT)
GPIO.setup(PWMB2, GPIO.OUT)
GPIO.setup(D1, GPIO.OUT)
GPIO.setup(D2, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
p1 = GPIO.PWM(D1, 500)
p2 = GPIO.PWM(D2, 500)
p1.start(25)
p2.start(25)


def set_motor(A1, A2, B1, B2):
    GPIO.output(PWMA1, A1)
    GPIO.output(PWMA2, A2)
    GPIO.output(PWMB1, B1)
    GPIO.output(PWMB2, B2)
    print("setting motors...")


def forward():
    set_motor(1, 0, 1, 0)
    print("going forward")


def stop():
    set_motor(0, 0, 0, 0)
    print("stop")


def reverse():
    set_motor(0, 1, 0, 1)
    print("reverse")


def left():
    set_motor(1, 0, 0, 0)
    print("left")


def right():
    set_motor(0, 0, 1, 0)
    print("right")


print("Distance measurement in progress")
GPIO.setwarnings(False)
GPIO.setup(TRIG, GPIO.OUT)  # Set pin as GPIO out
GPIO.setup(ECHO, GPIO.IN)  # Set pin as GPIO in


class MrBit_QTR_8RC:
    """ Class for reading values from Pololu QT8-8RC sensor array.
        Requires wiringpi https://github.com/WiringPi/WiringPi-Python
    """


    def __init__(self):
        """ Initialises class constants and variables - pins defined here.
        """

        self.wp = wp
        self.wp.wiringPiSetup()

        self.LEDON_PIN = 21
        self.SENSOR_PINS = [10, 3]
        self.NUM_SENSORS = len(self.SENSOR_PINS)
        self.CHARGE_TIME = 10  # us to charge the capacitors
        self.READING_TIMEOUT = 1000  # us, assume reading is black
        self.sensorValues = []
        self.calibratedMax = []
        self.calibratedMin = []
        self.lastValue = 0
        self.init_pins()


    def init_pins(self):
        """ Sets up the GPIO pins and also ensures the correct number of items
            in sensors values and calibration lists to store readings.
        """
        for pin in self.SENSOR_PINS:
            self.sensorValues.append(0)
            self.calibratedMax.append(0)
            self.calibratedMin.append(0)
            self.wp.pullUpDnControl(pin, self.wp.PUD_DOWN)
        self.wp.pinMode(self.LEDON_PIN, self.wp.OUTPUT)


    def emitters_on(self):
        """ Turns the LEDON pin on so that the IR LEDs can be turned on.
            If there is nothing wired to LEDON emitters will always be on.
            Use emitters_on and emitters_off to conserve power consumption.
        """
        self.wp.digitalWrite(self.LEDON_PIN, self.wp.HIGH)
        self.wp.delayMicroseconds(20)


    def emitters_off(self):
        """ Turns the LEDON pin off so that the IR LEDs can be turned off.
            If there is nothing wired to LEDON emitters will always be on.
            Use emitters_on and emitters_off to conserve power consumption.
        """
        self.wp.digitalWrite(self.LEDON_PIN, self.wp.LOW)
        self.wp.delayMicroseconds(20)


    def print_sensor_values(self, values):
        """ Params: values - a list of sensor values to print
            Prints out the sensor and it's current recorded reading.
        """
        for i in range(0, self.NUM_SENSORS):
            print("sensor %d, reading %d" % (i, values[i]))


    def initialise_calibration(self):
        """ Resets (inverse) max and min thresholds prior to calibration
            so that calibration readings can be correctly stored.
        """
        for i in range(0, self.NUM_SENSORS):
            self.calibratedMax[i] = 0
            self.calibratedMin[i] = self.READING_TIMEOUT


    def calibrate_sensors(self):
        """ Takes readings across all sensors and sets max and min readings
            typical use of this function is to call several times with delay
            such that a total of x seconds pass.  (e.g. 100 calls, with 20ms
            delays = 2 seconds for calibration).  When running this move the
            sensor over the line several times to calbriate contrasting surface.
        """
        for j in range(0, 10):
            self.read_sensors()
            for i in range(0, self.NUM_SENSORS):
                if self.calibratedMax[i] < self.sensorValues[i]:
                    self.calibratedMax[i] = self.sensorValues[i]
                if self.calibratedMin[i] > self.sensorValues[i] and self.sensorValues[i] > 30:
                    self.calibratedMin[i] = self.sensorValues[i]


    def read_line(self):
        """ Reads all calibrated sensors and returns a value representing a
            position on a line.  The values range from 0 - 7000, values == 0 and
            values == 7000 mean sensors are not on line and may have left the
            line from the right or left respectively.  Values between 0 - 7000
            refer to the position of sensor, 3500 referring to centre, lower val
            to the right and higher to the left (if following pin set up in init).
        """
        self.read_calibrated()

        avg = 0
        summ = 0
        online = False

        for i in range(0, self.NUM_SENSORS):
            val = self.sensorValues[i]
            if val > 500: online = True
            if val > 50:
                multiplier = i * 1000
                avg += val * multiplier
                summ += val

        if online == False:
            if self.lastValue < (self.NUM_SENSORS - 1) * 1000 / 2:
                return 0
            else:
                return (self.NUM_SENSORS - 1) * 1000

        self.lastValue = avg / summ
        return self.lastValue


    def read_calibrated(self):
        """ Reads the calibrated values for each sensor.
        """

        self.read_sensors()

        print("uncalibrated readings")
        self.print_sensor_values(self.sensorValues)

        for i in range(0, self.NUM_SENSORS):
            denominator = self.calibratedMax[i] - self.calibratedMin[i]
            val = 0
            if denominator != 0:
                val = (self.sensorValues[i] - self.calibratedMin[i]) * 1000 / denominator
            if val < 0:
                val = 0
            elif val > 1000:
                val = 1000
            self.sensorValues[i] = val

        print("calibrated readings")
        self.print_sensor_values(self.sensorValues)


    def read_sensors(self):
        """ Follows the Pololu guidance for reading capacitor discharge/sensors:
            1. Set the I/O line to an output and drive it high.
            2. Allow at least 10 us for the sensor output to rise.
            3. Make the I/O line an input (high impedance).
            4. Measure the time for the voltage to decay by waiting for the I/O
                line to go low.
            Stores values in sensor values list, higher vals = darker surfaces.
        """
        for i in range(0, self.NUM_SENSORS):
            self.sensorValues[i] = self.READING_TIMEOUT

        for sensorPin in self.SENSOR_PINS:
            self.wp.pinMode(sensorPin, self.wp.OUTPUT)
            self.wp.digitalWrite(sensorPin, self.wp.HIGH)

        self.wp.delayMicroseconds(self.CHARGE_TIME)

        for sensorPin in self.SENSOR_PINS:
            self.wp.pinMode(sensorPin, self.wp.INPUT)
            # important: ensure pins are pulled down
            self.wp.digitalWrite(sensorPin, self.wp.LOW)

        startTime = self.wp.micros()
        while self.wp.micros() - startTime < self.READING_TIMEOUT:
            time = self.wp.micros() - startTime
            for i in range(0, self.NUM_SENSORS):
                if self.wp.digitalRead(self.SENSOR_PINS[i]) == 0 and time < self.sensorValues[i]:
                    self.sensorValues[i] = time


# Example ussage:
if __name__ == "__main__":
    try:
        qtr = MrBit_QTR_8RC()

        approveCal = False
        while not approveCal:
            print("calibrating")
            qtr.initialise_calibration()
            qtr.emitters_on()
            for i in range(0, 250):
                qtr.calibrate_sensors()
                wp.delay(20)
                qtr.emitters_off()

                print("calibration complete")
                print("max vals")
                qtr.print_sensor_values(qtr.calibratedMax)
                print("calibration complete")
                print("min vals")
                qtr.print_sensor_values(qtr.calibratedMin)
                approved = raw_input("happy with calibrtion (Y/n)? ")
                if approved == ("Y"): approveCal = True

        while True:

            GPIO.output(TRIG, False)  # Set TRIG as LOW
            print("Waitng For Sensor To Settle")
            time.sleep(2)  # Delay of 2 seconds

            GPIO.output(TRIG, True)  # Set TRIG as HIGH
            time.sleep(0.00001)  # Delay of 0.00001 seconds
            GPIO.output(TRIG, False)  # Set TRIG as LOW

            while GPIO.input(ECHO) == 0:  # Check whether the ECHO is LOW
                pulse_start = time.time()  # Saves the last known time of LOW pulse

            while GPIO.input(ECHO) == 1:  # Check whether the ECHO is HIGH
                pulse_end = time.time()  # Saves the last known time of HIGH pulse

            pulse_duration = pulse_end - pulse_start  # Get pulse duration to a variable

            distance = pulse_duration * 17150  # Multiply pulse duration by 17150 to get distance
            distance = round(distance, 2)  # Round to two decimal points

            if distance < 30:
                print("Collision imminente")
                print("Distance:", distance - 0.5, "cm")
                stop()

            if qtr.sensorValue[1] > 350:
                print("going right")
                right()
            if qtr.sensorValue[0] > 350:
                print("going left")
                left()
            else:
                forward()

    except Exception as e:
        qtr.emitters_off()
        print(e)

    try:
        while 1:
            qtr.emitters_on()
            print(qtr.read_line())
            qtr.emitters_off()
            wp.delay(20)

    except KeyboardInterrupt:
        qtr.emitters_off()

    except Exception as e:
        print(e)