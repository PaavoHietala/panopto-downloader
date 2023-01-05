import os
from .config import config

def prepare_directories():
    '''Prepare required directories based on config.ini.'''

    for dir in ["playlist_dir", "video_dir"]:
        if not os.path.isdir(getattr(config, dir)):
            print("Creating dir", getattr(config, dir))
            os.makedirs(getattr(config, dir))
