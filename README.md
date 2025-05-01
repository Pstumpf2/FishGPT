# FishGPT
Modifying a 1999 Big Mouth Billy Bass to work with ChatGPT
## Note: if you have a more modern design (that uses 2 motors instead of 3), I would recommend [GoBig87's project, chat-gpt-raspberry-pi-assistant](https://github.com/GoBig87/chat-gpt-rasperry-pi-assistant)
# Run Through
Here's a video of the fish initializing, and running through a few prompts. Takes about a minute to start up on a Pi 3B.

https://github.com/user-attachments/assets/d669b875-19fe-48ec-9e78-5fddf758dd4a

(Note: the Pi3B we're using has 1GB of RAM, so most newer models should run significantly faster.)
# Wiring Digram
![diagram](https://github.com/user-attachments/assets/87a2add3-2c7b-485d-94b3-e5cdc9e3e48a)
# Setting up Fish GPT
## Parts
Links take you to the locations I bought parts.
- A 1999 Big Mouth Billy Bass [ebay, listing I purchased](https://www.ebay.com/itm/226452674546)
  - Components from the fish we’ll be using
    - The three motors that control head, tail, and mouth movement
    - The speaker
    - The button and it’s board
- A Raspberry Pi (this project uses a Pi 3, but any model should be fine. More ram should make queries faster though) [raspberrypi.com Raspberry Pi5](https://www.raspberrypi.com/products/raspberry-pi-5/)
- Two L98N H-Bridge Motor Shields [Amazon](https://a.co/d/cSF5fY6)
- A DC to DC Step Up Motor [Amazon](https://a.co/d/bhEAFac)
- 8+ Inch Pin Jumper Cables (Male to Male, Male to Female, Female to Female) [Amazon](https://a.co/d/0slArxf)
- Two USB Type C Power Supplies capable of at least 5 Volt power (I used the Steam Deck's chargers for this) [IFixit](https://www.ifixit.com/products/steam-deck-and-steam-deck-oled-ac-adapter-us)
- Two USB C ports with PD decoys [Amazon](https://a.co/d/btS0jl1)
- A USB Microphone [Adafruit](https://www.adafruit.com/product/3367)
- Items with alternative choices
  - A Mono-Channel AUX connector [Amazon](https://a.co/d/27kWA3g) if you plan on using the Bass’ speaker, and a Mono channel Amplifier [Adafruit](https://www.adafruit.com/product/2130)
    - Alternatively, a USB or Aux Speaker.
  - A Micro-USB to Type C Cable (or any cable with a male Micro-USB end that can transfer data) [Amazon](https://a.co/d/3EgrBZi)
    - Alternatively, if your Pi already supports Type C, A Type C Male to Female can be used, bypassing the second PD decoy USB C port.
## Tools
- A Soldering Station (Iron, solder, etc.)
- A PH2 Screwdriver or similarly sized screwdriver
- A Very Small Flathead Screwdriver
- A Multimeter
- Flush cutters
- Tools for setting up the Pi
  - A USB connected Keyboard and Mouse (for setting up the Pi)
  - An HDMI cable
  - A device to plug the HDMI into (TV, Monitor, etc.)
# Preparing the fish
1. Start by taking the single screw off the battery cover and remove any batteries inside.
    - You may need to clean rust from here as battery corrosion in such an old product isn’t unheard of.
2. Remove the six screws from the back of the plaque
3. Use gentle pressure to pop the back plate off. There aren’t any clips holding it on so removing the back should be easy. Note that the speaker, battery terminals, and motion toggle are attached to the back and could break off if you aren’t careful!
4. Remove the wires that connect the speaker, motors, motion toggle, and battery to the motherboard of the device. The closer you can cut to the motherboard, the more wire you’ll have to work with later. You can cut the wires off fully and solder on new ones, if you prefer.
    - (Optional) You can remove the battery terminals from the back by desoldering the wires and pushing the terminals through the other side with your flathead screwdriver or something similar.
5. Remove the DC 6V port from the device, as we will be using this area for powering the Pi and Motors. It should be held in by decades old hot glue, so it should come out with some gentle encouragement.
6. Once nothing is being held on by the motherboard, use a screwdriver to remove the screws holding it in and take it out.
7. Using flush cutters, remove the Screw ports and pins that held the motherboard, as we can use that spot for the Pi.
8. Along with that, use the cutters to flatten out the area the motion sensor was so we can use the spot for the microphone.
9. (Optional) For more space, you can use a dremel or flush cutters to remove the battery holder.

Once that is all taken care of, you should be able to get started working on adding in new parts!
# Installing the new hardware
## Note: I've placed them in order of importance, but for the most part you can do these in any order. **I reccomend reading each part first!**
## Raspberry Pi
- Until everything is put together and your software is set up, i'd suggest having it unattached for better maneuverability
- Once everything else is together, you can glue it to the bottom left of Billy's plaque.
  - I recommend using glue to hold it in rather than a heat set solution, as the plaque is thin. I got it to screw onto spacer held in with hot glue and Steel Stick Epoxy ([Amazon])(https://a.co/d/3jzGtAB). If you choose to do this, kkep in mind you will need to bend the pins a bit to have the back sit flush.
## USB C ports
- Take the Micro USB to Type C and remove the Type C end, exposing the 4 colored wires.
  - Red/Black = Power, Green/Blue = Data
- Solder the 4 wires onto one of the Type C ports.
- Take another one of the Type C ports, and configure the DIP switched to request 5 Volts (on the ports above, set 1 and 2 to 1 so its [1,1,0])
- connect two wires to the power terminals on the configured Type C port.
## Step Up
- Install near the USB C cables and connect the one configured to work with the motors to it using jumpers.
- Using a multimeter, Place the positive side on OUT+, and the negative side on OUT-.
- using a small screwdriver, adjust the output of the step up until it reaches 9 Volts.
## Motors
- Remove the jumper pins that connect enable a and enable b pins.
- Install your L928N H-bridges to the fish. A good spot I found is one above the motors and one to the top right of the case. Some hot glue should hold this in fine.
- Take the motor cables and connect them to the side screw on ports. One motor for each side.
- Connect 6 female to female jumper cables (first three are for motor A, last three are for motor B) to the entire bottom row of pins on the board
- Connect the other side of the jumper cables to the GPIO pins on the pi. Make sure each is on data pins, with the first and last cables on PWM enabled pins.
  - I used the pins [12, 19, 26, 5, 6, 13] for the Tail/Head
- For power, connect the 5V screw port to OUT+ on the step up
- connect GND to Out- on the step up
  - for the Head/Tail H Bridge, also connect GND to a GND pin on the Pi
- Repeat for the mouth motor, only using one motor port (so 3 data pins for Motor A or B. I use Motor B with the GPIO pins [26, 19, 12])
## Speaker(s)
### To preface, this uses the speaker that comes with the fish. If yours doesn’t work, or you'd prefer to pay more for an easier install, buy a USB speaker and plug it into the pi.
- Take the aux cable and connect it to the pi.
  - If you want it detachable from the speaker, attach male pin jumpers to the end.
  - Either way, you’ll need longer cables or to extend the cables.
- Get two Male to Male Jumper Cables and connect one to a 5V pin and one to a GND pin.
- Take the Speaker from the Bass and solder on cables, or use the ones already there and strip the ends
- Connect the ends into the mono audio amplifier. Match up + and - accordingly, then screw them into place.
- Connect the power pins and data pins to the amplifier (Power is Vin/GND, Data is D+/D-)
## Microphone
- Plug in the USB cable extender to the Pi
- Plug in the mic to the end of the USB extender
- Position the mic to where the motion sensor was, then glue it in.
  - Make sure the ribbon doesn't get pinched when reassembling it! you may want to glue it down in a spot or two.
# Setting up your SD Card
## To preface, have an [API Key](https://platform.openai.com/api-keys) for OpenAI and some funds for tokens! You'll need it later.
1. Flash Raspberry Pi OS onto your Micro SD Card and set it up.
    - Make sure WiFi is set up! It’s needed to connect to OpenAI and the code assumes WiFi is connected.
2. Download the files under release and place them in the location of your choice
3. In the root of the files, open config.py and configure it to your setup. The OpenAI API key needs configured or the code won't start!
4. Download the Small VOSK model (model 0.15), extract it, and place the folder in the model folder located in STT [Link](https://alphacephei.com/vosk/models). It should look like "[root of code]/STT/model/vosk-model-small-en-us-0.15"
5. Download piper_linux_x86_64.tar.gz from [Piper's release page](http://github.com/rhasspy/piper/releases/tag/2023.11.14-2), and place the extracted piper folder into the TTS folder. it should look like "[root of code]/TTS/piper"
6. Pick out [a voice to use](https://github.com/rhasspy/piper/blob/master/VOICES.md) and download it's json and onnx files. You can hear samples [here](https://piper.ttstool.com/). Make sure the files are named the same, and place them inside of the piper folder.
7. In the root of the code, using cmd, create a virtual environment named venv (You could name it something else or move it elsewhere, but then you’d have to change init.sh to reflect it)
    - Using Pi, to make a venv, open cmd and run this code: "python3 -m venv [location to make virtual environment]". as an example, mine is home/desktop/ as my code is placed on the desktop.
8. Once created, activate the venv in cmd by typing “source [root location of code]/venv/bin/activate”. You should now see (venv) to the left of your username in cmd.
9. Install the following dependencies in venv by using "pip install":
    - vosk
    - rpi-lgpio
    - gpiozero
    - sounddevice
    - pygame
  - alternatively, copy and paste the following line into cmd to install them all at once:
    ```
    pip install vosk rpi-lgpio gpiozero sounddevice pygame
    ```
9. Type “deactivate” to stop the virtual environment
10. Close cmd, then reopen again (or cd back to the root of the drive)
11. Type “sudo nano .bashrc“ to open bash.rc
    - It may prompt you on what editor to use. If it does, use nano
13. Scroll down to the end of the code, then add the following line so it launches on login:
“bash [root location of code]/init.sh”
14. Type ctrl+s to save it, then ctrl+x to close it
    - This will make the code init on startup, but also anytime cmd is started, so be warned!
15. Open up config.py and configure the variables to the ones you've set up
    - Most importantly API_KEY is needed to run ChatGPT! Code won't work without it
    - If you don't want to use GPT 4o-mini, change the model to the one you want to use
    - if you use different pins for GPIO, define them
    - Put the name of the voice you're using for Piper as well
    - the rest is optional, but change it if you wish.
# Cleanup
1. Put the back onto the plaque again, and screw it into place
2. Plug it in, and if everything's set up correctly, it should start on plug in after a minute or so!
## The code should now be ready to run!
# Modifying the code
The code is set up in a way where it's fairly modular, as long as the functions aren't renamed.
- The motors are set up in motor.py, as a class so they could be plucked from this and used to control Billy for any project (as long as the imports are brought with it)
- main.py imports speech_engine.py for initalization, and to call it's transcription function.
- A main brunt of the running occurs in speech_engine.py, including VOSK initialization, Motor setup, API_KEY checks, and the general process when VOSK successfully returns transcribed text.
- logger.py logs all transcribed text to the output folder in app.json, with timestamps.
- oai_gpt uses OpenAI's Responses API to run, essentially a function that takes the text from the transcription as input, uses a Billy-themed content briefing, uses the input text as user input, and returns ChatGPT's response.
- ai_tts uses Piper to run, using a system call to initialize and generate a .wav using a voice (in our case, us_john_medium). A followup function runs the defined .wav file, using pygame's get_busy() command to have Billy's mouth flap while talking.
# Thanks and Credits
This project was created for Kuo-pao Yang's CMPS 3750 class in Spring 2025. I want to thank my fellow team members, Adam Graves and Peyton Vinet!

If you want to see the showcase video, here it is! [YouTube](https://youtu.be/cvX9v3G8bKw)

I want to thank OpenAI for the easy to use API, Rhasspy's [Piper](https://github.com/rhasspy/piper) for it's optimized TTS for the Pi, Acephi's [VOSK](https://alphacephei.com/vosk/) for similar reasons to Piper, and James Bulpin's [article on hacking a Big Mouth Billy Bass](https://automateeverythingsite.wordpress.com/2016/11/20/hacking-big-mouth-billy-bass-part-13/) for its in depth coverage of Billys, along with timings for movements.

Finally, I want to shout out other inspirations and similar projects found during research, like [this Hackaday article that inspired the creation of this project](https://hackaday.com/2022/07/02/singing-fish-nails-sea-shanty-audition/) by Lewin Day, GoBig87's [chat-gpt-raspberry-pi-assistant](https://github.com/GoBig87/chat-gpt-rasperry-pi-assistant), and [GPTTARS](https://www.youtube.com/@gptars) for his silly Billy as well.

Thanks for reading!
