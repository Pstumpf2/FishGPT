#add parent directory as an import path
import sys
from os.path import dirname, abspath
parentDir = dirname(dirname(abspath(__file__)))
sys.path.insert(1, parentDir)
from config import PC_TEST
if not PC_TEST:
	from Motors.motor import mouth
from os import chdir, system, getcwd
import pygame
from multiprocessing import Process, Queue, Event
file_loc = getcwd()
def gen_piper(response):
	chdir(file_loc+"/TTS/piper") #head to the folder where piper is located
	system('echo "{0}" |   ./piper --model en_US-john-medium.onnx --output_file response.wav'.format(response))
	chdir(file_loc) #fix directory

def speak(filename, motor_mouth):
	queue = Queue()
	cont = Event()
	yap = Process(target = motor_mouth.talk_muppet, args = (cont,))
	chdir(file_loc+"/TTS/piper")
	pygame.mixer.init()
	out = pygame.mixer.Sound(filename+".wav")
	playing = out.play()
	while playing.get_busy():
		if not yap.is_alive():
			yap.start()
	cont.set()
	yap.join()
	motor_mouth.rest()
	chdir(file_loc)

def speak_nomotor(filename):
	chdir(file_loc+"/TTS/piper")
	pygame.mixer.init()
	out = pygame.mixer.Sound(filename+".wav")
	playing = out.play()
	while playing.get_busy():
		pygame.time.delay(100)
	chdir(file_loc)
