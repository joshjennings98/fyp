# main.py
from loadConfig import makeFromConfig
import sys


if __name__ == "__main__":

    if len(sys.argv) > 1:
        configFileLoc = sys.argv[1]
    else:   
        configFileLoc = 'network_generator/config'

    makeFromConfig(configFileLoc)