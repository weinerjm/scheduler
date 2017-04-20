import csv
import sys
import argparse
import calendar
import random
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument("input_file", type=str,
                     help="list of names")
parser.add_argument("output_file", type=str,
                    help="output file name")
parser.add_argument('-r', '--randomize',
                    dest='randomize', action='store_true',
                    default=False,
                    help='Randomize the assignments.')
parser.add_argument('-v', '--verbose',
                    dest='verbose', action='store_true',
                    default=False,
                    help='Enable debugging output.')

args = parser.parse_args()

# 'Sun' to 'Sat'
sun_to_sat = [list(calendar.day_abbr)[-1]] + list(calendar.day_abbr)[:-1]

# Code sequential weeks by appending '_1' and '_2'
day_names = [dayname+'_{}'.format(i) \
             for i in range(1,3) \
             for dayname in sun_to_sat]

def create_schedule():
    return {dayname:[] for dayname in day_names}

def assign_n_workers(pool, n):
    """Given a pool of possible man-hours (by ID) and the number of 
       employees to assign, return a list of unique IDs drawn from 
       the pool."""
    workers = []
    ctr = 0
    while len(workers) < n:
        ctr += 1
        curr_id = pool[0]
        if curr_id not in workers:
            workers.append(curr_id)
            pool.pop(0)
        else:
            random.shuffle(pool)
        if ctr > 1000:
            raise ValueError("Can't assign hours--incompatible possibilities!")
    # print "length of pool = ", len(pool)
    return list(sorted(workers)), pool

# Pick a day:
    # Choose a name/id from your "bag" (7*id for a 2-week period)
    # If the id isn't already on the day, then remove it from the "bag"
    # add it to the day
    # If the id IS working on the day,
    # put it back in the "bag" (do nothing)
    # but check the next ID
# When filled, advance to the next day.

# 1 on Sunday (rotates)
# 9 on Monday
# 12 on Tuesday (all employees)
# 9 on Wednesday
# 9 on Thursday 
# 10 on Friday
# 5 on Saturday
# 55 total spots.

# Excluding Sunday and Tuesday, everyone works 7 total slots over 
# two weeks.
def assign_all_workers(pool, schedule, cids):
    """Given a pool of possible man-hours, return a completed
       schedule."""
    for day_of_week, workers in schedule.iteritems():
        # print day_of_week
        if 'Fri' in day_of_week:
            schedule[day_of_week], pool = assign_n_workers(pool, 10)
        elif 'Tue' in day_of_week:
            schedule[day_of_week] = list(cids)
        elif 'Sat' in day_of_week:
            schedule[day_of_week], pool = assign_n_workers(pool, 5)
        elif 'Sun' in day_of_week:
            # do something special here
            pass
        else: # normal day
            schedule[day_of_week], pool = assign_n_workers(pool, 9)
    return schedule

def main():
    # Initialize an empty dictionary to store the lookup table
    id_to_name = {}

    # Load the name file
    print "Using {} as input file".format(args.input_file)
    with open(args.input_file, 'r') as infile:
        for cid, row in enumerate(csv.DictReader(infile)):
            id_to_name[cid] = row['name']

    cids = id_to_name.keys()
    pool = [cid for cid in cids for _ in xrange(7)]

    # Optional argument for full randomization
    if not args.randomize:
        random.seed(1)
    random.shuffle(pool) # randomize the placement

    finished = False
    iters = 0

    while not finished:
        iters += 1
        try:
            schedule = create_schedule()
            # Debug
            if args.verbose:
                print "pool size = ", len(pool)
            final_schedule = assign_all_workers(pool, schedule, cids)
            finished = True

            pprint(final_schedule)

            schedule_names = {day_of_week: [id_to_name[i] \
                                            for i in workers] \
                              for day_of_week, workers \
                              in final_schedule.iteritems()}
            # Final output
            pprint(schedule_names)

        except:
            # Debug
            if args.verbose:
                print "ERROR! Trying again!"
                print sys.exc_info()
                print schedule
            pool = [cid for cid in cids for _ in xrange(7)]
            random.shuffle(pool) # randomize the placement

        if iters % 10000 == 0 and args.verbose:
            print "ran {} iterations".format(iters)

    with open(args.output_file, 'w') as outfile:
        for dayname in day_names:
            outfile.write(dayname + ',' \
                          + ','.join(map(str,
                                         final_schedule[dayname])) \
                          + '\n')

    print "Wrote output to {}".format(args.output_file)

if __name__ == "__main__":
    main()
