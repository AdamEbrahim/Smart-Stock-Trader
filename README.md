# Smart-Stock-Trader
Standalone device that you can place on your desk to interact with the stock market and your trading portfolio in real time using voice control. This program can be run on a standard computer (MacOS, Windows, Linux) or a Raspberry Pi with a monitor and microphone. A PIR sensor and LED strip can optionally be used with the Raspberry Pi to enable the device to turn on and off based on if a user is in front of the device and to display whether or not the user's portfolio is at a profit or loss on the day. 

This program requires the user to have a registered Brokerage Account with Alpaca (https://alpaca.markets/). It can be used with both a real or paper trading account.

<img width=700 alt="IMG_2065" src="https://github.com/AdamEbrahim/Smart-Stock-Trader/assets/110650531/8f93b03c-5569-42f6-bade-953c73c827ce">

Functionality includes:
1. Turns on upon detecting your arrival and stays on until you leave
2. Complete voice control
3. View multiple stock graphs + current price
    - Real time updates when markets open through live websocket connections
    - Change time frame of stock graphs (1min, 1h, 1d, 1w, 1m, 1y, 5y)
    - Calibration updates based on if market is open or closed and time frame
4. Change (add, remove, replace) stocks on view with:
    - Specific stocks.
    - Top movers (gainers or losers)
    - Stocks in your portfolio
5. Execute market or limit trades (buy or sell) for any stock
    - Quantity of stocks or dollar value of stocks
    - Confirmation and invalid trade checking
    - Paper or real money
6. Green or red glow to signal portfolio gain or loss on the day, respectively


Demo Video:
1. Test2


## Installation
Follow the below instructions to install the necessary requirements to run the program. It is recommended to create a venv inside the overall directory and to download all pip dependencies in the venv. 

1. Whisper requires the command-line tool ffmpeg to be installed on your system, which is available from most package managers:

- on Ubuntu or Debian

```bash
sudo apt update && sudo apt install ffmpeg
```

- on Arch Linux

```bash
sudo pacman -S ffmpeg
```

- on MacOS using Homebrew (https://brew.sh/)

```bash
brew install ffmpeg
```

- on Windows using Chocolatey (https://chocolatey.org/)

```bash
choco install ffmpeg
```

- on Windows using Scoop (https://scoop.sh/)

```bash
scoop install ffmpeg
```


If there are errors while pip installing openai-whisper or tiktoken, Whisper may also require Rust. To install, follow this link: https://www.rust-lang.org/learn/get-started


2. The real-time speech recognition software requires pyaudio to be installed on your system:

- on Windows:

```bash
pip install pyaudio
```

- on MacOS:

```bash
brew install portaudio
pip install pyaudio
```

- on GNU/Linux (Inlcudes Raspberry Pi):

```bash
sudo apt-get install python3-pyaudio
sudo apt-get install python3-dev
sudo apt-get install portaudio19-dev
pip install pyaudio
```


3. After completing the above, to install the required dependencies run: 

- On Windows or MacOS:
```bash
pip install -r requirements.txt
```

- On Raspberry Pi (if not using LED strip or PIR sensor):
```bash
pip install -r requirements.txt
```

- On Raspberry Pi (if using LED strip and PIR sensor):
```bash
pip install -r rpi_requirements.txt
```

## Configuration and Wiring (Raspberry Pi Only)
If using a raspberry pi configure display settings by running:

1. sudo raspi-config
2. Select "Display Options"
3. Select "Screen Blanking"
4. Disable Screen Blanking

If choosing to connect a PIR sensor and LED strip, connect the PIR sensor signal pin to the desired GPIO pin and the LED strip data pin to one of GPIO10, GPIO12, GPIO18, or GPIO21.

Currently, NeoPixel requires sudo to run on the Raspberry Pi. However, sudo can disable proper microphone input detection. Thus, it is recommended to connect the LED strip data pin to GPIO10 (board.D10) and to run the following:

1. sudo raspi-config
2. Select "Interface Options"
3. Select "SPI"
4. Enable SPI

This will allow the program to run properly without sudo.

## Config File
To put necessary environment variables, such as trading API keys, make a copy of "config_template.yml" and name it "config.yml". Fill in the following fields in "config.yml" depending on OS/Device:

- On Windows or MacOS:
LIVE_API_KEY - PAPER_SECRET_KEY (get through Alpaca dashboard)

- On Linux (Including Raspberry Pi without LED strip or PIR sensor):
LIVE_API_KEY - GUI_SETUP_TIME

- On Raspberry Pi with LED strip and PIR Sensor:
LIVE_API_KEY - MONITOR_TIMEOUT

A description of the config.yml fiels is below:
LIVE_API_KEY: From Alpaca
LIVE_SECRET_KEY: From Alpaca
PAPER_API_KEY: From Alpaca
PAPER_SECRET_KEY: From Alpaca
MONITOR_RESOLUTION: Width x Height (ex: "800x480")
GUI_SETUP_TIME: Make a bit longer than time it takes for GUI to setup.
PIR_PIN: PIR signal pin (GPIO.BCM Configuration)
LED_PIN: LED Strip data pin (GPIO.BCM Configuration)
LED_PIXELS: Number of pixels in LED strip
MONITOR_TIMEOUT: Minutes before device turns off after detecting user has left.

## Running
Finally, run the program using:

```bash
python3 mainTesting.py
```

## Voice Control Commands
The voice commands must follow the structures below to achieve the desired functionality. Any words in brackets are meant to be replaced with the user's desired inputs. Any brackets with quotations signal that the user should choose one of the options inside the quotations.

1. Add [Stock Name] - Adds a stock to the view
2. Remove [Stock Name] - Removes a stock from the view
3. Replace [Stock Name To Remove] [Stock Name To Add] - Replaces a stock with another stock
4. Change Time Frame [Stock Name] [Time Frame] - Changes the time frame of a stock graph. Time frames include: "Minute" (1min), "hour" (1h), "day" (1d), "week" (1w), "month" (1m), "year" (1y), and "max" (5y)
5. View Top Movers ["gainers", "losers"] - Displays the top gainers or losers of the day in the view
6. View Portfolio - Displays stocks in the user's portfolio in the view
7. Market ["purchase", "sale"] ["quantity", "value"] [QtyOrValue #/Price] [Stock Name] - Executes a market trade for a stock. The user can choose to input the quantity of stocks or the dollar value of stocks to trade. 
8. Limit ["purchase", "sale"] ["quantity", "value"] [QtyOrValue #/Price] Limit [Limit Price] [Stock Name] - Executes a limit trade for a stock. The user can choose to input the quantity of stocks or the dollar value of stocks to trade. The user must also input the limit price of the trade.
