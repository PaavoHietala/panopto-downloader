import json
import time
import re
import urllib

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

from .config import config

def get_ts_url(stream_url):
    print(f'Downloading stream {stream_url}')

    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    options.binary_location = config.chrome_path

    ser = Service(config.webdriver_path)
    driver = webdriver.Chrome(service=ser, options = options)
    driver.get(stream_url)
    time.sleep(1)
    driver.find_element(By.ID, "playButton").click()
    title = driver.title

    def process_browser_log_entry(entry):
        response = json.loads(entry['message'])['message']
        return response

    while True:
        browser_log = driver.get_log('performance') 
        events = [process_browser_log_entry(entry) for entry in browser_log]
        events = [event for event in events if 'Network.response' in event['method']]

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
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')

    return text

def ts_to_m3u8(url, title):
    print(f'Downloading playlist for "{title}"\n')

    base = "/".join(url.split("/")[:-2])
    master_url = base + "/master.m3u8"

    master = get_file_as_string(master_url).split("\n")
    index_url = f"{base}/{master[2].strip()}"

    index = get_file_as_string(index_url)
    index = re.sub("(.*.ts)", f"{'/'.join(index_url.split('/')[:-1])}/\\1", index)

    print('Done')

    return index  
