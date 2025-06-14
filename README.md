# Spotify Downloader GUI

![Main UI Screenshot](https://i.ibb.co/0j7ZDksD/image.png)

A user-friendly desktop application for downloading tracks, albums, and playlists from Spotify as high-quality MP3 files.

## Features

-   **Intuitive GUI**: A clean and modern interface for easy navigation.
-   **Download Queue**: Add multiple Spotify links and download them sequentially.
-   **Playlist Management**: Select specific songs from a playlist before you download.
-   **Quality Selection**: Choose your preferred audio quality based on file size.
-   **Duplicate Check**: Avoid re-downloading songs you already have.
-   **Cross-Platform**: Compatible with Windows and Linux.

---

## Getting Started

### 1. Download the Latest Release

Grab the latest version from the [**Releases Page**](https://github.com/pgwiz/SYDownloader/releases). The download comes as a `.7z` archive containing everything you need to run the application.

-   [**Spotify-Downloader-v1.0.7z**](https://github.com/pgwiz/SYDownloader/releases/download/v1.0.7z/SY-Downloader-v1.0.7z)

### 2. How to Run

1.  **Extract the Archive:** Unzip the `Spotify-Downloader-v1.0.7z` file.
2.  **Run the Application:** Execute `main.exe` from the extracted folder.
3.  **For Linux open terminal in the folder then run**
    ```bash
    chmod +x * && ./main.exe
    ```
    *Even though its exe its compiled with python so it will run*
4.  **Ensure `ffmpeg.exe` is present:** The application relies on `ffmpeg.exe` for audio conversion. Make sure it is in the same directory as `main.exe`. or u can set it on path

---

## How it Works

The application takes a Spotify URL and uses a custom backend API to find the corresponding YouTube video IDs. It then uses the powerful `yt-dlp` library to download and convert the audio into an MP3 file, which is saved to the `spotify_downloads` folder.

For a complete breakdown of all features and setup instructions, please view the [**Full Documentation**](https://spotify.cyring.store).

## Building from Source

If you prefer to run the application directly from the source code:

1.  **Prerequisites:**
    * Python 3.8+
    * FFmpeg

2.  **Clone the repository:**
    ```bash
    git clone https://github.com/pgwiz/SYDownloader.git SYD
    cd SYD
    ```

3.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate      # On Windows

    pip install -r requirements.txt
    ```
    *(Note: You will need to create a `requirements.txt` file containing `customtkinter`, `httpx`, and `Pillow`)*

4.  **Run the application:**
    ```bash
    python main.py
    ```
