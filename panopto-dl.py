import os
from src import playlist, utils
from src.config import config

def download_stream(url):
    ts_url, title = playlist.get_ts_url(url)
    index_m3u8 = playlist.ts_to_m3u8(ts_url, title)

    with open(os.path.join(config.playlist_dir, f'{title}.m3u8'), "w") as f:
        f.write(index_m3u8)

utils.prepare_directories()

if config.args.stream:
    download_stream(config.args.stream)
elif config.args.file:
    with open(config.args.file, 'r') as f:
        urls = f.readlines()
    
    for url in urls:
        download_stream(url)
else:
    print("No stream URLs given...")
