import threading
from multiStockView import multiStockView
from stockObject import stockObject
from alpaca.data.timeframe import TimeFrameUnit
import alpacaAPI
from utilities import checkValidStock

#used for voice control:
import argparse
import numpy as np
import speech_recognition as sr
import whisper
import torch
import string

from datetime import datetime, timedelta, timezone
from queue import Queue
from time import sleep
from sys import platform

#ui stuff
from view import view

class stockTrader:

    #paperTrading = true if paper trading session, false otherwise, dim = tuple (x,y) of stock UI dimensions, 
    def __init__(self, api_key, secret_key, paperTrading, dim):
        self.api_key = api_key
        self.secret_key = secret_key
        self.paperTradingSession = paperTrading
        self.dim = dim

        #used for voice control, Only necessary for leveled commands
        self.prevCommands = []

        self.UI = view(dim)

        #create multiStockView object
        self.stockList = multiStockView(self.api_key, self.secret_key, 60, self.UI, dim)
        currStock = stockObject(api_key, secret_key, "AAPL", TimeFrameUnit.Day, self.stockList.multiStockUI)
        # threading.Thread(target=self.stockList.addStock, args=[currStock]).start()
        self.stockList.addStock(currStock)
        currStock = stockObject(api_key, secret_key, "GOOG", TimeFrameUnit.Day, self.stockList.multiStockUI)
        self.stockList.addStock(currStock)
        currStock = stockObject(api_key, secret_key, "MSFT", TimeFrameUnit.Day, self.stockList.multiStockUI)
        self.stockList.addStock(currStock)

        #set up thread for listening for voice commands and operating on them (kind of the "main thread" in a sense)
        threading.Thread(target=self.setupVoiceControl).start()

        #this works, can only call mainloop with main thread i think
        self.UI.tk.mainloop()

    


    def handleVoiceCommand(self, command):
        #self.stockList.stocks[0].stockUI.changeContents(self.stockList.stocks[0].data)

        #have received first level command
        if len(self.prevCommands) > 0:
            #can break out of any command sequence using keyword "exit"
            lowercmd = command.casefold()
            if "exit" in lowercmd:
                self.prevCommands.clear() #clear list of cmds
                return
            
            stockName = 0

            #first level command is for trading and have gotten stock name to trade
            if self.prevCommands[0] == "trade" and len(self.prevCommands) > 1:
                print("hi")

                self.prevCommands.clear() #clear list of cmds
                return
            
            #first level command is for changing timeframe and have gotten stock name
            elif self.prevCommands[0] == "timeframe" and len(self.prevCommands) > 1:
                timeInterval = 0
                if "minute" in lowercmd:
                    timeInterval = TimeFrameUnit.Minute
                elif "hour" in lowercmd:
                    timeInterval = TimeFrameUnit.Hour
                elif "day" in lowercmd:
                    timeInterval = TimeFrameUnit.Day
                elif "week" in lowercmd:
                    timeInterval = TimeFrameUnit.Week
                elif "month" in lowercmd:
                    timeInterval = TimeFrameUnit.Month
                elif "year" in lowercmd:
                    timeInterval = "oneYear"
                elif "max" in lowercmd: #MAX IS HOW YOU GET 5 YEAR COMMAND
                    timeInterval = "fiveYear"


                obj = self.stockList.stocksDict.get(self.prevCommands[1])
                if obj != None:
                    obj.changeTimeInterval(timeInterval)
                else:
                    print("stock to change timeframe of is not a current stock")

                self.prevCommands.clear() #clear list of cmds
                return


            #remove punctuation from stock name if any
            stockName = command.translate(str.maketrans('', '', string.punctuation))
            stockName = stockName.upper() #stock names should be upper case
            print(stockName)

            #make sure it is a valid stock name
            if not checkValidStock(self.api_key, self.secret_key, stockName):
                print("invalid stock name")
                return
            
            #replace, timeframe, trade all require a stock name after first command
            if len(self.prevCommands) == 1 and (self.prevCommands[0] == "replace" or self.prevCommands[0] == "timeframe" or self.prevCommands[0] == "trade"):
                self.prevCommands.append(stockName)
                return

            #execute the first level command based on stock name for view commands (not change timeframe)
            match self.prevCommands[0]:
                case "add":
                    currStock = stockObject(self.api_key, self.secret_key, stockName, TimeFrameUnit.Day, self.stockList.multiStockUI)
                    self.stockList.addStock(currStock)
                    self.prevCommands.clear() #make sure to reset prevCommands
                case "remove":
                    self.stockList.removeStock(stockName)
                    self.prevCommands.clear() #make sure to reset prevCommands
                case "replace":
                    currStock = stockObject(self.api_key, self.secret_key, stockName, TimeFrameUnit.Day, self.stockList.multiStockUI)
                    self.stockList.replaceStock(self.prevCommands[1], currStock)
                    self.prevCommands.clear() #make sure to reset prevCommands
                    
            return

        #BELOW ONLY EXECUTED IF WE HAVEN'T RECEIVED A FIRST LEVEL COMMAND
        cmd = command.casefold() #get lower case command (for case insensitive comparison)
        #1st level commands: view specific stocks
        if "add" in cmd:
            self.prevCommands.append("add")

        elif "remove" in cmd:
            self.prevCommands.append("remove")

        elif "replace" in cmd:
            self.prevCommands.append("replace")

        #1st level command: change timeframe
        if "time frame" in cmd:
            self.prevCommands.append("timeframe")

        #1st level commands: trade stocks
        elif "trade" in cmd:
            self.prevCommands.append("trade")


        #just view individual portfolio, no need for leveled commands
        elif "view portfolio" in cmd:
            print("hi")

        #view top movers (gainers or losers), no need for leveled commands
        elif "top movers" in cmd:
            if "gain" in cmd:
                alpacaAPI.getTopMovers(self.api_key, self.secret_key, self.stockList, "gain")
            elif "loss" in cmd or "lose" in cmd:
                alpacaAPI.getTopMovers(self.api_key, self.secret_key, self.stockList, "loss")
    
            


    def setupVoiceControl(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--model", default="tiny", help="Model to use",
                            choices=["tiny", "base", "small", "medium", "large"])
        parser.add_argument("--non_english", action='store_true',
                            help="Don't use the english model.")
        parser.add_argument("--energy_threshold", default=1000,
                            help="Energy level for mic to detect.", type=int)
        parser.add_argument("--record_timeout", default=2,
                            help="How real time the recording is in seconds.", type=float)
        parser.add_argument("--phrase_timeout", default=3,
                            help="How much empty space between recordings before we "
                                "consider it a new line in the transcription.", type=float)
        if 'linux' in platform:
            parser.add_argument("--default_microphone", default='pulse',
                                help="Default microphone name for SpeechRecognition. "
                                    "Run this with 'list' to view available Microphones.", type=str)
        args = parser.parse_args()

        # The last time a recording was retrieved from the queue.
        phrase_time = None
        # Thread safe Queue for passing data from the threaded recording callback.
        data_queue = Queue()
        # We use SpeechRecognizer to record our audio because it has a nice feature where it can detect when speech ends.
        recorder = sr.Recognizer()
        recorder.energy_threshold = args.energy_threshold
        # Definitely do this, dynamic energy compensation lowers the energy threshold dramatically to a point where the SpeechRecognizer never stops recording.
        recorder.dynamic_energy_threshold = False

        # Important for linux users.
        # Prevents permanent application hang and crash by using the wrong Microphone
        if 'linux' in platform:
            mic_name = args.default_microphone
            if not mic_name or mic_name == 'list':
                print("Available microphone devices are: ")
                for index, name in enumerate(sr.Microphone.list_microphone_names()):
                    print(f"Microphone with name \"{name}\" found")
                return
            else:
                for index, name in enumerate(sr.Microphone.list_microphone_names()):
                    if mic_name in name:
                        source = sr.Microphone(sample_rate=16000, device_index=index)
                        break
        else:
            source = sr.Microphone(sample_rate=16000)

        # Load / Download model
        model = args.model
        if args.model != "large" and not args.non_english:
            model = model + ".en"
        audio_model = whisper.load_model(model)

        record_timeout = args.record_timeout
        phrase_timeout = args.phrase_timeout

        transcription = ['']

        with source:
            recorder.adjust_for_ambient_noise(source)

        def record_callback(_, audio:sr.AudioData) -> None:
            """
            Threaded callback function to receive audio data when recordings finish.
            audio: An AudioData containing the recorded bytes.
            """
            # Grab the raw bytes and push it into the thread safe queue.
            data = audio.get_raw_data()
            data_queue.put(data)

        # Create a background thread that will pass us raw audio bytes.
        # We could do this manually but SpeechRecognizer provides a nice helper.
        recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

        # Cue the user that we're ready to go.
        print("Model loaded.\n")

        while True:
            try:
                now = datetime.now(timezone.utc)
                # Pull raw recorded audio from the queue.
                if not data_queue.empty():
                    phrase_complete = False

                    if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                        phrase_complete = True
                    # This is the last time we received new audio data from the queue.
                    phrase_time = now
                    
                    # Combine audio data from queue
                    audio_data = b''.join(data_queue.queue)
                    data_queue.queue.clear()
                    
                    # Convert in-ram buffer to something the model can use directly without needing a temp file.
                    # Convert data from 16 bit wide integers to floating point with a width of 32 bits.
                    # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
                    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                    # Read the transcription.
                    result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                    text = result['text'].strip()

                    # If we detected a pause between recordings, add a new item to our transcription.
                    # Otherwise edit the existing one.
                    if phrase_complete:
                        transcription.append(text)
                    else:
                        transcription[-1] = text


                    print(transcription[-1])
                    self.handleVoiceCommand(transcription[-1])

                else:
                    sleep(0.25)
            except KeyboardInterrupt:
                break

        print("\n\nTranscription:")
        for line in transcription:
            print(line)