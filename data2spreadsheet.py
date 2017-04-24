################################
'''
Converts output.txt to a csv file that is stored in the output directory
'''
################################

import csv
import itertools
import sys
import os

f = open('output.txt', 'r')

def write_file(in_file, name):
    outputDir = "output/" #Output directory
    os.system("mkdir -p %s"%(outputDir)) #Create directory if doesn't exist

    out_file = open(outputDir+name, 'w')
    
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)

    writer = csv.writer(out_file)
    writer.writerows(lines)

    out_file.close()

def convert():
    # Find handle of data
    handle = f.readline()
    handle = handle.strip()
    handle = handle[19:]
    print(handle)

    date = f.readline()
    date = date.strip()
    date = date[16:]
    print(date)

    date = date.split()
    date = '_'.join(date)
    name = 'output_' + handle + '_' + date + '.csv'
    print('Writing to file %s...' %(name))
    write_file(f, name)
    print('Complete.')

    f.close()
convert()
