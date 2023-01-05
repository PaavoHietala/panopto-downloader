import json
import time
import re
import urllib
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

from .config import config

def get_ts_url(stream_url):
    '''
    Find the URL for a single video chunk for given Panopto stream.
    
    As the master playlist and the streamed chunks are hidden from the user
    using a secret token in the data URLs, the video chunk URL containing the
    token is figured by capturing a video chunk request from the player. 

    Parameters
    ----------
    stream_url : str
        URL of the Panopto stream to download.

    Returns
    -------
    str
        URL of a single video chunk containing the token. If a playlist with
        retrieved title exists, the URL will be None.
    str
        Title of the requested Panopto video (=webpage title).
    '''

    print(f'\nDownloading stream {stream_url}')

    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.binary_location = config.chrome_path

    ser = Service(config.webdriver_path)
    driver = webdriver.Chrome(service = ser, options = options)
    driver.get(stream_url)
    time.sleep(.5)
    driver.find_element(By.ID, "playButton").click()
    title = driver.title

    if check_playlist_exists(title):
        return None, title

    i = 0
    while True:
        i += 1
        print(f'Capturing a video chunk{"." * (i % 3 + 1)}', end = '\r')
        browser_log = driver.get_log('performance') 
        events = [json.loads(log['message'])['message'] for log in browser_log]
        events = [e for e in events if 'Network.response' in e['method']]

        found = False
        for e in events:
            try:
                if e['params']['response']['url'].endswith('.ts'):
                    url = e['params']['response']['url']
                    print(f'Got playlist url for "{title}"')
                    found = True
                    break
            except KeyError:
                continue
    
        if found:
            driver.quit()
            break
    
    return url, title

def get_file_as_string(url):
    '''
    Download a text file in given URL and return it as a string.

    Parameters
    ----------
    url : str
        URL of the text file (in this case .m3u8 file).

    Returns
    -------
    str
        Contents of the text file.
    '''

    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')

    return text

def check_playlist_exists(title):
    '''
    Check if a playlist with given title exists in the configured playlist dir
    and if the overwrite flag is set.

    Returns False if the file does not exist or it is allowed to be overwritten.

    Parameters
    ----------
    title : str
        Name of the playlist without the extension .m3u8.

    Returns
    -------
    Bool
        True if file exists and overwrite == False, False otherwise.
    '''

    playlist_path = os.path.join(config.playlist_dir, f'{title}.m3u8')
    
    if os.path.isfile(playlist_path) and config.args.overwrite == False:
        print(f'Playlist {title}.m3u8 already exists. Use option -o to overwrite.')
        return True

    return False

def ts_to_m3u8(url, title):
    '''
    Retrieve a playlist corresponding to the given video chunk URL.

    Parameters
    ----------
    url : str
        URL of a single video chunk.
    title : str
        Title of the Panopto stream webpage, used for file naming.

    Returns
    -------
    str
        Content of the playlist corresponding to the given video chunk.
    '''

    print(f'Downloading playlist for "{title}"')

    base = "/".join(url.split("/")[:-2])
    master_url = base + "/master.m3u8"

    master = get_file_as_string(master_url).split("\n")
    index_url = f"{base}/{master[2].strip()}"

    index = get_file_as_string(index_url)
    index = re.sub("(.*.ts)", f"{'/'.join(index_url.split('/')[:-1])}/\\1", index)

    return index  

def download_playlist(ts_url, title):
    '''
    Download a .m3u8 playlist corresponding to the given video chunk.

    Parameters
    ----------
    ts_url : str
        URL of a single video chunk.
    title : str
        Title of the Panopto stream webpage, used for file naming.
    '''

    playlist_path = os.path.join(config.playlist_dir, f'{title}.m3u8')
    
    if not check_playlist_exists(title):
        index_m3u8 = ts_to_m3u8(ts_url, title)

        with open(playlist_path, "w") as f:
            f.write(index_m3u8)
