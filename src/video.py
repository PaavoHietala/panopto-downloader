import os
import requests
from .config import config

def extract_urls(title):
    '''
    Extract video chunk URLs from given playlist.

    Parameters
    ----------
    title : str
        Name of the playlist without the .m3u8 extension.

    Returns
    -------
    list of str
        List of all video chunk URLs in order.
    '''

    m3u8_path = os.path.join(config.playlist_dir, f'{title}.m3u8')

    with open(m3u8_path, 'r') as f:
        m3u8 = f.readlines()
    
    return [line.strip() for line in m3u8 if line.startswith('https://')]

def download_video(title):
    '''
    Download a complete video from given playlist.

    Parameters
    ----------
    title : str
        Name of the playlist without the .m3u8 extension.
    '''

    max_attempts = 5
    out_path = os.path.join(config.video_dir, f'{title}.ts')
    urls = extract_urls(title)
    
    if os.path.isfile(out_path) and config.args.overwrite == False:
        print(f'File {title}.ts already exists. Use option -o to overwrite.')
        return

    print(f'Downloading "{title}.ts"')

    with open(out_path, 'wb') as f:
        for url_idx, url in enumerate(urls):
            success = False
            
            for i in range(max_attempts):
                try:
                    segment = b''
                    for chunk in requests.get(url, stream = True):
                        segment += chunk
                    success = True
                    break
                except (ConnectionError, requests.HTTPError):
                    print(f'Failed to retrieve segment {url_idx + 1}/{len(urls)} \
                          , retrying ({i+1}/{max_attempts})...', end = '\r')

            if not success:
                print(f'Failed to download video {title}')
                break
            else:
                f.write(segment)
                print(f'Wrote segment {url_idx + 1}/{len(urls)}', end = '\r')
    
    if not success:
        os.remove(out_path)
    else:
        print(f'Downloaded "{title}.ts" successfully!')
