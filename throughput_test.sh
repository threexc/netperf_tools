#!/bin/bash

# This script runs the netperf command and creates a logfile consisting of the
# same results as echoed back to the user

#netperf_command="netperf -H10.222.68.5 -l360 -p 12236 -- -m 90000 -M 90000 -S 90000 -s 90000"
netperf_command="netperf"
total=0
count=$1

echo "Running $count iterations of netperf"
date_val=`date`

# Replace whitespace in the date variable with underscores
date_stripped=${date_val// /_}
log_filename=`echo "netperf_log_${date_stripped}_${count}_iterations"`
echo "netperf performance test run at $log_time" >> $log_filename
echo "Number of iterations: $count" >> $log_filename

for i in `seq 1 $count`;
do
  # Get the 5th column of the last row of output (throughput value) and put it
  # in an array
  throughput_values[i]=`netperf | awk '{print $5}' | tail -1`

  # Sum up the successive array values for the average
  total=`echo "${throughput_values[i]}+$total" | bc`
  echo "Iteration $i throughput measurement was ${throughput_values[i]} Mbits/sec"
  echo "Iteration $i throughput measurement was ${throughput_values[i]} Mbits/sec" >> $log_filename
done

# Use bc again to get the average throughput
average=`echo "scale=2; $total/$count" | bc`

echo "Average throughput calculated at $average Mbits/sec over $count iterations"
echo "Log file created as $log_filename"

echo "Average throughput calculated at $average Mbits/sec over $count iterations" >> $log_filename
