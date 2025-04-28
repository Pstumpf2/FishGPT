#add parent directory as an import path
import sys
from os.path import dirname, abspath
parentDir = dirname(dirname(abspath(__file__)))
sys.path.insert(1, parentDir)
from config import MODEL_PATH, SAMPLE_RATE, BLOCK_SIZE, CHANNELS, DTYPE, BUTTON_PIN, PC_TEST, API_KEY, MODEL
from GPT.oai_gpt import Chat
from TTS.ai_tts import *
from STT.logger import log_message

from sys import exit
import json
import os
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from multiprocessing import Process, Queue, Event


    
# --- Audio Queue ---
q = queue.Queue()

# --- Setup Model ---
print("Loading Model...")
model = Model(os.path.abspath("STT/"+MODEL_PATH))
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
print("Model Loaded.")

if not PC_TEST:
    # --- Setup GPIO (for RPi) ---
    from Motors.motor import *
    from gpiozero import Button
    BillyButton = Button(BUTTON_PIN)
    Head = head()
    Mouth = mouth()
    Tail = tail()
    if(API_KEY == ""):
        print("You have not replaced the API key for Open AI! Please go do that.")
        speak("noKey", Mouth)
        exit(1)
    else:
        speak("init", Mouth) 
elif (API_KEY == ""):
    print("You have not replaced the API key for Open AI! Please go do that.")
    speak_nomotor("noKey")
    exit(1)
else:
    speak_nomotor("init")
# --- Microphone Callback ---
def callback(indata, frames, time, status):
    if status:
        print(f"[Audio Error]: {status}")
    q.put(bytes(indata)) # puts audio into the queue

# --- Transcription Loop ---
def transcribed_from_mic():
    try:
        first_time=False
        while True:
            if PC_TEST:
                input("\n[SIMULATED] Press Enter to record, or Ctrl+C to quit...")
            else:
                print("Waiting for Button press...")
                BillyButton.wait_for_press()
                print("Button pressed!")
                Head.move(100)
            text = transcribe_from_mic()
            if text:
                if not PC_TEST:
                    Head.rest()
                    queue = Queue()
                    flapstop = Event()
                    fishflap = Process(target = Tail.flap_inf, args = (flapstop,)) #needs to be declared in while statement to avoid running the same process twice. If you add parenthases, then the func is called instead of being used as a target.
                    fishflap.start() #starts the process of fishflap
                    print(f'\tYou: "{text}"')
                    response = Chat(text)
                    print(f'\t{MODEL}: "{response}"')
                    gen_piper(response)
                    flapstop.set()
                    fishflap.join()
                    Tail.rest()
                    Head.move(100)
                    speak("response", Mouth)
                    Head.rest()
                else:
                    print(f'\tYou: "{text}"')
                    response = Chat(text)
                    print(f'\t{MODEL}: "{response}"')
                    gen_piper(response)
                    speak_nomotor("response")
            else:
                print("No valid speech detected.")
                if not PC_TEST:
                    speak("error", Mouth)
                    Head.rest()
                else:
                    speak_nomotor("error")
    except KeyboardInterrupt:
        print("\n[Shutdown] Exiting...")
        if not PC_TEST:
            motor.stop()

# --- Transcribe Audio ---
def transcribe_from_mic():
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        dtype=DTYPE,
        channels=CHANNELS,
        callback=callback
    ):
        print("[Listening] Speak now...")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                log_message(result)
                return result.get("text", "").strip()
