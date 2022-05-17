import os
import util
import argparse

FILEPATH = os.path.dirname('/mnt/d/Collectivat/ladino/Ladino_STT/')
RAW_PATH = os.path.join(FILEPATH, 'alignment-resources/raw')
PROC_PATH = os.path.join(FILEPATH, 'alignment-resources/process')


def main():
    
    parser = argparse.ArgumentParser("Parse Text and WAV")
    parser.add_argument("-p", "--path", help="Project's path.")
    args = parser.parse_args()
    FILEPATH = args.path
    util.text_wav_normalized(FILEPATH)
    
if __name__ == '__main__':
    main()
