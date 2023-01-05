import argparse
import os
import configparser

class _Config:
    def __init__(self):
        cfgpath = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               'config.ini')

        if os.path.isfile(cfgpath):
            self.config = configparser.ConfigParser()
            self.config.read(cfgpath)
        else:
            raise FileNotFoundError("config.ini not found")

        parser = argparse.ArgumentParser()
        inputs = parser.add_mutually_exclusive_group()
        inputs.add_argument('-s', '--stream', help = 'A single Panopto stream \
                            URL to download')
        inputs.add_argument('-f', '--file', help = 'A text file with Panopto \
                            stream URLs to download.')
        inputs.add_argument('-o', '--overwrite', action = 'store_true',
                            help = 'Overwrite existing files.')

        self.args = parser.parse_args()


    def __getattr__(self, name):
        try:
            return self.config.get("DEFAULT", name)
        except KeyError:
            print(f"Config does not have the attribute '{name}'")

config = _Config()