import threading
from multiStockView import multiStockView
from stockObject import stockObject
from alpaca.data.timeframe import TimeFrameUnit

#used for voice control:
import argparse
import numpy as np
import speech_recognition as sr
import whisper
import torch

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

        self.UI = view(dim)
        #thread to deal with the blocking UI stuff
        #threading.Thread(target=self.UI.tk.mainloop).start()

        #create multiStockView object
        self.stockList = multiStockView(self.api_key, self.secret_key, 60, self.UI, dim)
        #currStock = stockObject(api_key, secret_key, "AAPL", TimeFrameUnit.Week, self.stockList.multiStockUI)
        # threading.Thread(target=self.stockList.addStock, args=[currStock]).start()
        #self.stockList.addStock(currStock)

        #set up thread for listening for voice commands and operating on them (kind of the "main thread" in a sense)
        threading.Thread(target=self.setupVoiceControl).start()

        #this works, can only call mainloop with main thread i think
        self.UI.tk.mainloop()


    def handleVoiceCommand(self, command):
        if command == "add" or command == "Add." or command == "Ad.":
            currStock = stockObject(self.api_key, self.secret_key, "AAPL", TimeFrameUnit.Week, self.stockList.multiStockUI)
            self.stockList.addStock(currStock)
        elif command == "remove" or command == "Remove." or command == "remove.":
            print("hey")
            self.stockList.removeStock("AAPL")
            


    def setupVoiceControl(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--model", default="base", help="Model to use",
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
                    # If enough time has passed between recordings, consider the phrase complete.
                    # Clear the current working audio buffer to start over with the new data.
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
                    # Infinite loops are bad for processors, must sleep.
                    sleep(0.25)
            except KeyboardInterrupt:
                break

        print("\n\nTranscription:")
        for line in transcription:
            print(line)