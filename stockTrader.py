import voiceControl
import threading

class stockTrader:

    def __init__(self, api_key, secret_key):

        #set up thread for listening for voice commands
        threading.Thread(target=voiceControl.main).start()