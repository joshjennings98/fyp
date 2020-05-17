# main.py
from loadConfig import makeFromConfig
import random
import sys


if __name__ == "__main__":

    random.seed(123)
    
    if len(sys.argv) > 1:
        configFileLoc = sys.argv[1]
    else:   
        configFileLoc = '../config'

    makeFromConfig(configFileLoc)
