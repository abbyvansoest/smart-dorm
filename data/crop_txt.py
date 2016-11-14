import sys
import os
from os import listdir
from os.path import isfile, join
import re

def afterNinth(date):
    string = date.split("-")
    month =  int(string[1])
    day = int(string[2])

    if (month >= 9 and day > 8):    
        return True
    else:
        return False

mypath = 'data/before_school/'
dir_name = 'data/before_school/txt/'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

if '.DS_Store' in files: files.remove('.DS_Store')

# Open each file and crop all data after 9/8/16
for f in files:
    txt_file_name, extension = os.path.splitext(f)
    txtfile = open(mypath+f, "r")

    if not txtfile.closed:
        text_list = [];
        for line in txtfile.readlines():
            line = re.sub('[\"]', '', line)
            line = line.split(",", 3)
            if (line[0] == 'DateAndTime'): 
                continue
            print "line[0]  " + line[0]
            date = line[0].split(" ")
            print "date[0] " + date[0]
            if afterNinth(date[0]): break
            text_list.append("\t".join(line))
        txtfile.close()

    txt_file = open(dir_name+txt_file_name+".txt", "w")

    if not txt_file.closed:
        for line in text_list:
            txt_file.write(line)
        print('File Successfully written.')
        txt_file.close()