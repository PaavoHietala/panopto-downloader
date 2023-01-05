from src import playlist, utils, video
from src.config import config

def download_stream(url):
    '''
    Download a playlist and a video file from given Panopto stream page.

    Parameters
    ----------
    url : str
        URL of the Panopto stream page to download.
    '''

    ts_url, title = playlist.get_ts_url(url)

    if ts_url:
        playlist.download_playlist(ts_url, title)
    
    video.download_video(title)

if __name__ == '__main__':
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
