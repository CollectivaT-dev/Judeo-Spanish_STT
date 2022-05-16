import os
import util
import argparse


def main():
    parser = argparse.ArgumentParser("Parse Text")
    parser.add_argument("-f", "--file", help="file to be normalized.")
    args = parser.parse_args()
    
    path_file = args.file
    path_write = path_file[:-4]+"_norm.txt"
    with open(path_write, 'w') as file_w:
        with open(path_file) as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() != "":
                    line = util.normalizer(line)
                    numbers = [int(s.replace(".","").replace(",","")) for s in line.split() if s.replace(".","").replace(",","").isdigit()]
                    for number in numbers:
                        line = line.replace(str(number),(util.num_let(number)))
                    file_w.write(line+"\n")


if __name__ == '__main__':
    main()
