#!/usr/bin/python3

import subprocess
import datetime
import json
import os
import sys

# args should be a list of string arguments for the netperf program
def netperf_parse(args):

    # Variable to hold the output of netperf
    netperf_output = ""
    # Create a list for collecting all of the lines anyway in case the input
    # arguments and objectives change for new performance tests
    netperf_lines = []

    # Run netperf and pipe its output
    netperf_proc = subprocess.Popen(args, stdin=subprocess.PIPE, \
    stdout=subprocess.PIPE, stderr=None, shell=False)

    # Get the stdout data from the process and decode it
    netperf_output = netperf_proc.communicate()[0]
    netperf_output = netperf_output.decode('utf-8')

    # Add the decoded data to the list
    for line in netperf_output.splitlines():
        netperf_lines.append(line)

    # Get the throughput value (last value) by splitting the last line
    return netperf_lines[-1].split()[-1]

# Logs the arguments used and the throughput average to a time-stamped log file
# in JSON format
def log_throughput(json_data):

    # Create the log directory if it doesn't exist
    if not os.path.exists("netperf_logs"):
        os.mkdir("netperf_logs")

    # Create a string for the log file name
    logfile = "netperf_logs/netperf_throughput_" + json_data['date'] + ".json"

    # Dump the json data passed to this function
    with open(logfile, 'w') as f:
        json.dump(json_data, f, indent=4)
    f.close()

# Calculate the average throughput over a given number of iterations. Prints the
# individual throughput results as it works for debug purposes
def get_average_throughput(iterations, netperf_args):

    # list for storing the results from each run
    throughput_values = []

    # Run the tests and print each individual throughput value
    for iteration in range(iterations):
        throughput_values.append(float(netperf_parse(netperf_args)))
        print("Test {0} throughput was {1:.2f} Mbits/s\n".format(iteration+1,\
        throughput_values[iteration], ".2f"))

    # Calculate and return the average
    average_throughput = sum(throughput_values) / len(throughput_values)
    return average_throughput

# Check to see if the default options (i.e. arguments given in the test) are
# intended. Otherwise, run netperf with no arguments. A more advanced version
# of this script would use the argparse library (or at least a more
# sophisticated if-else list) and be more flexible with inputting
# netperf options. Could also clean up the prints into another function
if __name__ == '__main__':

    # Two argument lists for netperf
    full_args = ["netperf", "-H10.222.68.5", "-l360", "-p", "12236", "--",\
     "-m", "90000", "-M", "90000", "-S", "90000", "-s", "90000"]
    default_args = ["netperf", "-H127.0.0.1", "-l30"]

    # Get the timestamp for use in the log file
    date = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    date = date.replace(' ', '_')
    date = date + " (UTC)"

    #
    print("Starting test run with timestamp {0}\n".format(date))
    if len(sys.argv) == 3:
        if sys.argv[2] == "full":
            result = get_average_throughput(int(sys.argv[1]), full_args)
            json_data = {}
            json_data['date'] = date
            json_data['args'] = full_args
            json_data['throughput'] = result
            json_data['iterations'] = sys.argv[1]
            print("Average throughput calculated as {0:.2f} Mbits/s over {1} iterations\n".format(result, sys.argv[1]))
            log_throughput(json_data)

        else:
            print("Incorrect netperf options specified.\n")
    elif len(sys.argv) == 2:
        result = get_average_throughput(int(sys.argv[1]), default_args)
        json_data = {}
        json_data['date'] = date
        json_data['args'] = full_args
        json_data['throughput'] = result
        json_data['iterations'] = sys.argv[1]
        print("Average throughput calculated as {0:.2f} Mbits/s over {1} iterations\n".format(result, sys.argv[1]))
        log_throughput(json_data)
    else:
        print("Incorrect number of arguments specified. Must specify number of\
 iterations followed by \"qnx\" or other appropriate option.\n")
