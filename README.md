# Randomized Scheduler

1. Run 

`python schedule.py names.csv schedule_out.csv [--randomize]` 

where `names.csv` is a single-column `.csv` file with the column named `name` and 12 entries below. You can replace the file names with any files you want.
The `--randomize` flag randomizes the output.

2. Look at the output in `schedule_out.csv`.

3. Randomly assign names to the slots using the command:

`python assign_names.py names.csv schedule_out.csv named_schedule_out.csv`

and look for the named assignments in `named_schedule_out.csv`. Note that it overwrites the output file by default, so be careful!

Again, these filenames can be anything.
