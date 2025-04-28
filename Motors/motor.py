#add parent directory as an import path
import sys
from os.path import dirname, abspath
parentDir = dirname(dirname(abspath(__file__)))
sys.path.insert(1, parentDir)
from config import MOTOR_PINS, PC_TEST
from multiprocessing import Event

import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
class motor:
	def __init__(self,pin1,pin2,pinEnable):
		self.pin1 = pin1 #set pins for the class, used later
		self.pin2 = pin2
		self.enable = pinEnable
		GPIO.setup(self.pin1,GPIO.OUT) #setup the gpio pins to recognize the pins
		GPIO.setup(self.pin2,GPIO.OUT)
		GPIO.setup(self.enable,GPIO.OUT)
		self.power = GPIO.PWM(self.enable,1000)
		GPIO.output(self.pin1, GPIO.LOW) #reset to make sure no motors move on init
		GPIO.output(self.pin2,GPIO.LOW)
		self.power.start(100)
	def move(self, pow):
		self.power.ChangeFrequency(pow)
		GPIO.output(self.pin1,GPIO.HIGH)
		GPIO.output(self.pin2,GPIO.LOW)
	def rest(self):
		GPIO.output(self.pin1,GPIO.LOW)
		GPIO.output(self.pin2,GPIO.LOW)
	def stop():
		GPIO.cleanup()
class head(motor):
	def __init__(self):
		super().__init__(MOTOR_PINS["head"]["in1"],MOTOR_PINS["head"]["in2"],MOTOR_PINS["head"]["enable"])
		
class tail(motor):
	def __init__(self):
		super().__init__(MOTOR_PINS["tail"]["in1"],MOTOR_PINS["tail"]["in2"],MOTOR_PINS["tail"]["enable"])
	def flap(self, cycles=1):
		for x in range(cycles):
			tail.move(self,pow=100)
			sleep(0.25)
			tail.rest(self)
			sleep(0.2)
	def rest(self):
		GPIO.output(self.pin1,GPIO.LOW)
		GPIO.output(self.pin2,GPIO.LOW)
	def flap_inf(self, cont):
		while not cont.is_set():
				GPIO.output(self.pin1,GPIO.HIGH)
				GPIO.output(self.pin2,GPIO.LOW)
				sleep(0.25)
				GPIO.output(self.pin1,GPIO.LOW)
				GPIO.output(self.pin2,GPIO.LOW)
				sleep(0.2)
		
		
class mouth(motor):
	def __init__(self):
		super().__init__(MOTOR_PINS["mouth"]["in1"],MOTOR_PINS["mouth"]["in2"],MOTOR_PINS["mouth"]["enable"])
	def talk_muppet(self, cont):
		while not cont.is_set():
				GPIO.output(self.pin1,GPIO.HIGH)
				GPIO.output(self.pin2,GPIO.LOW)
				sleep(0.4)
				GPIO.output(self.pin1,GPIO.LOW)
				GPIO.output(self.pin2,GPIO.LOW)
				sleep(0.35)
		self.rest()
