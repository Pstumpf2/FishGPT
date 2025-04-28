#add parent directory as an import path
import sys
from os import path, makedirs
parentDir = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.insert(1, parentDir)
from config import API_KEY, MODEL
from openai import OpenAI

def Chat(toOAI):
  client = OpenAI(api_key=API_KEY)
  #using the newer OpenAI response API
  response = client.responses.create(
    model=MODEL,
    input=[
      {
        "role": "system",
        "content": [
          {
            "type": "input_text",
            "text": "You are a 1999 Gemmy Big Mouth Billy Bass animatronic, equipped to listen and respond at the press of your button. You are a silly assistant who will receive a prompt and respond in a helpful, humorous manner. Your response is being sent through a Text to Speech, so please refrain from using emojis or similar items that could break it. Along with that, you are not configured to retain conversations, so avoid responses that would need a response back."
          }
        ]
      },
      {
        "role": "user",
        "content":[
            {
                "type": "input_text",
                "text": toOAI
            }
        ]
      }
    ],
    text={
      "format": {
        "type": "text"
      }
    },
    reasoning={},
    tools=[],
    temperature=1,
    max_output_tokens=2048,
    top_p=1,
    store=True #You can check history in the Dashboard on OpenAI's API login.
  )
  return (response.output_text)
