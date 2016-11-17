# A simple program to create a formatted text file from a *.csv file.

import sys
import os
from os import listdir
from os.path import isfile, join
import re

def get_name(index):

    if (index == 1):
        return 'tuesday/first/'
    if (index == 2):
        return 'tuesday/second/'
    if (index == 3):
        return 'tuesday/third/'
    if (index == 4):
        return 'weds/first/'
    if (index == 5):
        return 'weds/second/'
    if (index == 6):
        return 'weds/third/'
    if (index == 7):
        return 'thurs/first/'
    if (index == 8):
        return 'thurs/second/'
    if (index == 9):
        return 'thurs/third/'
    if (index == 10):
        return 'friday/first/'
    if (index == 11):
        return 'friday/second/'
    if (index == 12):
        return 'friday/third/'
    if (index == 13):
        return 'saturday/first/'
    if (index == 14):
        return 'saturday/second/'
    if (index == 15):
        return 'saturday/third/'
    if (index == 16):
        return 'sunday/first/'
    if (index == 17):
        return 'sunday/second/'
    if (index == 18):
        return 'sunday/third/'

    return 'NOPE/'


done = False
index = 1
while (index <= 18):

    mypath = get_name(index)
    dir_name = mypath

    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    if '.DS_Store' in files: files.remove('.DS_Store')

    for f in files:
        txt_file_name, extension = os.path.splitext(f)
        name_split =  txt_file_name.split(" ")
        name = name_split[0]
        csv_file = open(mypath+f, "r")


        if not csv_file.closed:
            text_list = [];
            for line in csv_file.readlines():
                line = re.sub('[\"]', '', line)
                line = line.split(",", 3)
                if (line[0] == 'DateAndTime'): 
                    continue
                text_list.append("\t".join(line))
            csv_file.close()

        txt_file = open(dir_name+name+".txt", "w")

        if not txt_file.closed:
            for line in text_list:
                txt_file.write(line)
            print('File Successfully written.')
            txt_file.close()

    index = index + 1







