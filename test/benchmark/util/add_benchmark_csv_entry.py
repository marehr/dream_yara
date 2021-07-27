#!/usr/bin/env python3

# Example:
# python ./add_benchmark_csv_entry.py \
#        ./yara_mapper.time.json \
#        ./yara_mapper.log.json \
#        --append-to-csv ./benchmark_csv_file.csv

def merge_time_and_yara_mapper_log_files(time_log, yara_mapper_log):
    return {**time_log, **yara_mapper_log}

def csv_field_names():
    return [
        'current_time',

        'ibf_load_time',
        'ibf_reads_filter_time',
        'reads_copy_time',
        'aignments_copy_time',
        'cigar_move_time',

        'fm_index_total_time',
        'fm_index_genome_load_time',
        'fm_index_reads_load_time',
        'fm_index_seed_time',
        'fm_index_filter_time',
        'fm_index_classification_time',
        'fm_index_rank_time',
        'fm_index_entension_time',
        'fm_index_sort_time',
        'fm_index_compact_time',
        'fm_index_alignment_time',
        'fm_index_output_time',
        'total_reads',
        'mapped_reads',
        'avg_reads_per_bin',

        'command', 'exit_status', 'user_time', 'system_time', 'cpu_percent', 'wall_clock_time', 'max_resident_set_size',
        'major_page_faults', 'minor_page_faults', 'file_system_inputs', 'file_system_outputs',
        'voluntary_context_switches', 'involuntary_context_switches',
        'thread_count'
    ]

if __name__ == "__main__":
    import argparse
    import json

    from pathlib import Path
    from datetime import datetime, timezone

    parser = argparse.ArgumentParser()
    parser.add_argument('time_log_json_file', metavar='<time log json file>', type=Path, help='The output of ./parse_time_log.py')
    parser.add_argument('yara_mapper_log_json_file', metavar='<yara mapper log json file>', type=Path, help='The output of ./parse_yara_mapper_log.py')
    parser.add_argument('--append-to-csv', metavar='<csv file>', type=Path, help='Append parsed benchmark result to CSV file.', required=True)

    args = parser.parse_args()

    # print json file
    with open(args.time_log_json_file) as json_file:
        time_log = json.load(json_file)
    with open(args.yara_mapper_log_json_file) as json_file:
        yara_mapper_log = json.load(json_file)

    merged = merge_time_and_yara_mapper_log_files(time_log, yara_mapper_log)
    merged['current_time'] = datetime.now(timezone.utc).isoformat()

    import csv

    write_header = not args.append_to_csv.exists()

    with open(args.append_to_csv, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_field_names(), extrasaction='ignore')

        if write_header:
            writer.writeheader()
        writer.writerow(merged)

    print ("{} csv entry in file {} ".format("Created" if write_header else "Appended", args.append_to_csv))
