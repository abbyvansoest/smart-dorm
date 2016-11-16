# A simple program to create a formatted text file from a *.csv file.

import sys
import os
from os import listdir
from os.path import isfile, join
import re

mypath = 'data/by_weekday/'
dir_name = 'data/by_weekday/txt/'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

if '.DS_Store' in files: files.remove('.DS_Store')

for f in files:
    txt_file_name, extension = os.path.splitext(f)
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

    txt_file = open(dir_name+txt_file_name+".txt", "w")

    if not txt_file.closed:
        for line in text_list:
            txt_file.write(line)
        print('File Successfully written.')
        txt_file.close()