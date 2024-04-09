# Smart-Stock-Trader
Standalone device that you can place on your desk to interact with the stock market and your trading portfolio in real time


To install the required dependencies run: 
pip install -r requirements.txt

Whisper also requires the command-line tool ffmpeg to be installed on your system, which is available from most package managers:

# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg


If there are errors while pip installing openai-whisper or tiktoken, Whisper may also require Rust. To install, follow this link: https://www.rust-lang.org/learn/get-started


The real-time speech recognition software also requires pyaudio to be installed on your system:

# on Windows:
pip install pyaudio

# on MacOS:
brew install portaudio
pip install pyaudio

# on GNU/Linux (Inlcudes Raspberry Pi):
sudo apt-get install python3-pyaudio
