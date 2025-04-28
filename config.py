#Open AI
API_KEY = "" #Get this from your OpenAI API account.
MODEL="gpt-4o-mini"
#Physical Input
BUTTON_PIN = 2
MOTOR_PINS = {
    "mouth": {
        "enable": 25,  #Make sure each enable is a PWM compatible Pin.
        "in1": 24,  #You may have to swap in1 and in2 if the motor isn't moving right.
        "in2": 23 
    },
    "head": {
        "enable": 13,
        "in1": 6,
        "in2": 5
    },
    "tail": {
        "enable": 12,
        "in1": 19,
        "in2": 26
    }
}
PC_TEST = False # Set True to test on PC. Skips all motor functions and replaces Button input with Enter on a keyboard.
#VOSK and Piper
MODEL_PATH = "model/vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000
BLOCK_SIZE = 8000
DTYPE = "int16"
CHANNELS = 1
LOG_FOLDER = "Output"
PIPER_MODEL = "en_US-john-medium"
