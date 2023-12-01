# Panopto video downloader

This command line tool can be used to download videos (lecture recordings etc.) from Panopto.

## Installation

1. Install required packages using
    ```
    python -m pip install -r requirements.txt
    ```
2. Download the correct ChromeDriver for your platform and Chrome version [here](https://chromedriver.chromium.org/downloads).
3. Verify the settings (especially chrome_path and webdriver_path) in `config.ini`. By default the config file looks like this:
    ```
    [DEFAULT]
    chrome_path=C:\Program Files\Google\Chrome\Application\chrome.exe   # Location of chrome.exe
    webdriver_path=.\chromedriver.exe                                   # Location of chromedriver.exe
    playlist_dir=.\playlists                                            # Downloaded stream playlist destination
    video_dir=.\videos                                                  # Downloaded video destination
    ```

    Both relative and absolute paths can be used. By default the webdriver is expected to be placed in the repository folder.

## Usage

The program is used via command line. The playlist corresponding to the requested video is saved in `playlist_dir` defined in `config.ini`. Likewise the final `.ts` videos are saved in `video_dir`.

### Downloading a single video

A single URL for a Panopto stream can be given as an argument:
```
python panopto-dl.py -s <stream url>
```

### Downloading multiple videos

One can also give a list of video URLs as a text file (one URL per line) with option `-f`:
```
python panopto-dl.py -f <file_with_urls.txt>
```

### Overwrite protection

By default the files are protected from accidental overwrites. To enable overwriting, use the option `-o`:

```
python panopto-dl.py -s <stream url> -o
```

### Command line arguments

The basic arguments include
```
usage: panopto-dl.py [-h] [-s STREAM | -f FILE | -o]

options:
  -h, --help                show this help message and exit
  -s, --stream <url>        A single Panopto stream URL to download
  -f, --file <filename.txt> A text file with Panopto stream URLs to download.
  -o, --overwrite           Overwrite existing files.
```
