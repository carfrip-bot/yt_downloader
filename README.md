# YouTube Downloader GUI

A simple GUI developed in Python using **PySide6** to download videos and audio from YouTube at the highest possible quality, leveraging the power of **yt-dlp**.

The application features a native dark theme, a real-time progress bar, and handles downloads in the background using dedicated threads to prevent the interface from freezing.


## 🚀 Features

* **Maximum Resolution Download:** Automatically merges the best available video and audio streams (up to 4K/8K) into an `.mkv` container.
* **Pre-configured Quality Profiles:** Quickly select standard formats (MP4 at 1080p or 720p) to save storage space.
* **Audio Extraction:** Download the audio track directly, converting it to `MP3` format at the highest quality (320 kbps).
* **Output Destination Management:** Freely choose your preferred save folder via an intuitive directory selection button.
* **Smooth Progress Bar:** Monitor download progress in real time without cluttering the process log window.


## 🛠️ Requirements & Installation

To run this application, you need to install the required Python libraries and the essential system tool **FFmpeg**.

### 1. Save the Script

Make sure you have your `yt_downloader.py` file and the `yt_downloader.png` icon file located in the same directory.

### 2. Install Python Libraries

Open your terminal or command prompt inside the project folder and install the necessary packages via `pip`:

```bash
pip install PySide6 yt-dlp

```

* **PySide6:** Handles the graphical user interface.
* **yt-dlp:** The core engine that downloads the videos.

### 3. Install FFmpeg (CRITICAL)

`yt-dlp` requires **FFmpeg** to merge high-definition video tracks (which YouTube serves separately from audio) and to convert audio streams into MP3 format.

#### 🪟 Windows

The fastest way is using the Windows Package Manager (run this in Command Prompt or PowerShell as Administrator):

```cmd
winget install Gyan.FFmpeg

```

*Alternatively, download the binaries from the official FFmpeg website and manually add the `bin` folder to your system's Environment Variables (PATH).*

#### 🍏 macOS

Via Homebrew:

```bash
brew install ffmpeg

```

#### 🐧 Linux

Via your distribution's package manager (e.g., Ubuntu/Debian):

```bash
sudo apt update && sudo apt install ffmpeg

```


## 💻 Usage

1. If you haven't already, generate a compatible icon file using the conversion script, or simply ensure `yt_downloader.png` is in the directory.
2. Launch the main application:

```bash
python yt_downloader.py

```

3. Paste the YouTube video URL into the input field.
4. Select your destination folder (it defaults to your system's *Downloads* folder).
5. Choose your desired quality profile and click **DOWNLOAD**.


## 🔧 Troubleshooting

* **The download fails immediately or won't merge audio/video:** Verify that FFmpeg is properly installed by running `ffmpeg -version` in your terminal. If the command is not recognized, FFmpeg is not configured in your system's PATH.
* **Videos stop downloading / YouTube errors occur:** YouTube constantly updates its platform to block downloaders. If you encounter errors, update the underlying `yt-dlp` engine by running:
```bash
pip install --upgrade yt-dlp

```