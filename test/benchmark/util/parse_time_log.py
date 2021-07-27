#!/usr/bin/env python3

# Example:
# python ./parse_time_log.py ./yara_mapper.time > ./yara_mapper.time.json

def parse_time_log(path):
    result = dict()
    with open(path) as f:
        for line in f:
            if line.startswith('\tCommand being timed'):
                #	Command being timed: "./bin/dream_yara_mapper --bloom-filter ./test/benchmark/data/benchmark1/19_1G.filter --output-file 19_1G_100.sam --threads 4 --error-rate 0.03 --verbose --version-check 0 ./test/benchmark/data/benchmark1/fm-indices/ ./test/benchmark/data/benchmark1/reads_e2_100.fastq"
                components = line.split(': ', 2)[1].strip().strip('"')
                result['command'] = components
            if line.startswith('\tUser time'):
                #	User time (seconds): 107.75
                components = line.split(': ', 2)[1].strip()
                result['user_time'] = components
            if line.startswith('\tSystem time'):
                #	System time (seconds): 3.09
                components = line.split(': ', 2)[1].strip()
                result['system_time'] = components
            if line.startswith('\tPercent of CPU this job got'):
                #	Percent of CPU this job got: 364%
                components = line.split(': ', 2)[1].strip()
                result['cpu_percent'] = components.rstrip('%')
            if line.startswith('\tElapsed (wall clock) time'):
                #	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:30.44
                components = line.split(': ', 2)[1].strip()
                time_components = components.split(':')
                hours = 0
                if len(time_components) == 3:
                    hours, minutes, seconds = time_components
                if len(time_components) == 2:
                    minutes, seconds = time_components
                # convert to seconds
                result['wall_clock_time'] = 24 * 60 * float(hours) + 60 * float(minutes) + float(seconds)
            if line.startswith('\tAverage shared text size'):
                #	Average shared text size (kbytes): 0
                components = line.split(': ', 2)[1].strip()
                result['avg_shared_text_size'] = components
            if line.startswith('\tAverage unshared data size'):
                #	Average unshared data size (kbytes): 0
                components = line.split(': ', 2)[1].strip()
                result['avg_unshared_data_size'] = components
            if line.startswith('\tAverage stack size'):
                #	Average stack size (kbytes): 0
                components = line.split(': ', 2)[1].strip()
                result['avg_stack_size'] = components
            if line.startswith('\tAverage total size'):
                #	Average total size (kbytes): 0
                components = line.split(': ', 2)[1].strip()
                result['avg_total_size'] = components
            if line.startswith('\tMaximum resident set size'):
                #	Maximum resident set size (kbytes): 1389200
                components = line.split(': ', 2)[1].strip()
                result['max_resident_set_size'] = components
            if line.startswith('\tAverage resident set size'):
                #	Average resident set size (kbytes): 0
                components = line.split(': ', 2)[1].strip()
                result['avg_resident_set_size'] = components
            if line.startswith('\tMajor (requiring I/O) page faults'):
                #	Major (requiring I/O) page faults: 1808
                components = line.split(': ', 2)[1].strip()
                result['major_page_faults'] = components
            if line.startswith('\tMinor (reclaiming a frame) page faults'):
                #	Minor (reclaiming a frame) page faults: 621727
                components = line.split(': ', 2)[1].strip()
                result['minor_page_faults'] = components
            if line.startswith('\tVoluntary context switches'):
                #	Voluntary context switches: 753
                components = line.split(': ', 2)[1].strip()
                result['voluntary_context_switches'] = components
            if line.startswith('\tInvoluntary context switches'):
                #	Involuntary context switches: 1079
                components = line.split(': ', 2)[1].strip()
                result['involuntary_context_switches'] = components
            if line.startswith('\tSwaps'):
                #	Swaps: 0
                components = line.split(': ', 2)[1].strip()
                result['swaps'] = components
            if line.startswith('\tFile system inputs'):
                #	File system inputs: 0
                components = line.split(': ', 2)[1].strip()
                result['file_system_inputs'] = components
            if line.startswith('\tFile system outputs'):
                #	File system inputs: 0
                components = line.split(': ', 2)[1].strip()
                result['file_system_outputs'] = components
            if line.startswith('\tSocket messages sent'):
                #	Socket messages sent: 0
                components = line.split(': ', 2)[1].strip()
                result['socket_messages_sent'] = components
            if line.startswith('\tSocket messages received'):
                #	Socket messages received: 0
                components = line.split(': ', 2)[1].strip()
                result['socket_messages_received'] = components
            if line.startswith('\tSignals delivered'):
                #	Signals delivered: 0
                components = line.split(': ', 2)[1].strip()
                result['signals_delivered'] = components
            if line.startswith('\tPage size'):
                #	Page size (bytes): 4096
                components = line.split(': ', 2)[1].strip()
                result['page_size'] = components
            if line.startswith('\tExit status'):
                #	Exit status: 0
                components = line.split(': ', 2)[1].strip()
                result['exit_status'] = components
    return result

if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument('time_log_file', metavar='<time log file>', type=Path, help='The output of /usr/bin/time -v -o <time log file>.')

    args = parser.parse_args()

    # print json file
    print(json.dumps(parse_time_log(args.time_log_file)))
