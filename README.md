# Smart-Stock-Trader
Standalone device that you can place on your desk to interact with the stock market and your trading portfolio in real time


Run “pip install -r requirements.txt” to install the required libraries
The speech recognition tool used in this project, openai/whisper, requires the following additional tools to be installed:

1. ffmpeg:
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

2. Rust (only if errors while pip installing openai-whisper):
Follow this link: https://www.rust-lang.org/learn/get-started
