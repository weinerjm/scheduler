import csv
import sys
import argparse
import calendar
import random
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument("name_file", type=str,
                     help="list of names")
parser.add_argument("schedule_file", type=str,
                    help="schedule setup file")
parser.add_argument("output_file", type=str,
                    help="output file name")
args = parser.parse_args()

def main():
    names = []
    print "Using {} as name file".format(args.name_file)
    with open(args.name_file, 'r') as infile:
        for row in csv.DictReader(infile):
            names.append(row['name'])
 
    random_ids = range(len(names))
    random.shuffle(random_ids)

    id_to_name = {cid: name for cid, name in zip(random_ids,
                                                 names)}

    with open(args.schedule_file, 'r') as schedfile, \
         open(args.output_file, 'w') as outfile:
        for line in schedfile:
            row = line.strip().split(',')
            dayname, values = row[0], row[1:]
            out_names = [id_to_name[int(i)] for i in values \
                         if len(i) > 0] 
            outfile.write(dayname + ',' \
                          + ','.join(out_names) \
                          + '\n')

    print "Wrote output to {}".format(args.output_file)

if __name__ == "__main__":
    main()
