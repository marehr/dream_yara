#!/usr/bin/env python3

# Example:
# python ./parse_yara_mapper_log.py ./yara_mapper.log > ./yara_mapper.log.json

def parse_yara_mapper_log(path):
    result = dict()
    with open(path) as f:
        for line in f:
            if line.startswith('Threads count'):
                # Threads count:			4
                components = line.split(':')[1]
                result['thread_count'] = int(float(components))
            if line.startswith('Filter loading time'):
                # Filter loading time:		0.827543 sec		2.53359 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['ibf_load_time'] = float(components.rstrip(' sec'))
            if line.startswith('Reads filtering time'):
                # Reads filtering time:		9.25455 sec		28.3335 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['ibf_reads_filter_time'] = float(components.rstrip(' sec'))
            if line.startswith('Reads copying time'):
                # Reads copying time:		0.0780516 sec		0.238961 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['reads_copy_time'] = float(components.rstrip(' sec'))
            if line.startswith('Alignments copying time'):
                # Alignments copying time:	1.04535 sec		3.20042 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['aignments_copy_time'] = float(components.rstrip(' sec'))
            if line.startswith('Cigars moving time'):
                # Cigars moving time:		0.273786 sec		0.838216 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['cigar_move_time'] = float(components.rstrip(' sec'))
            if line.startswith('Total time'):
                # Total time:			32.6629 sec
                components = line.split(':')[1].strip().split('\t')[0]
                result['fm_index_total_time'] = float(components.rstrip(' sec'))
            if line.startswith('Genome loading time'):
                # Genome loading time:		0.0282316 sec		0.0864333 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['fm_index_genome_load_time'] = float(components.rstrip(' sec'))
            if line.startswith('Reads loading time'):
                # Reads loading time:		1.15997 sec		3.55134 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['fm_index_reads_load_time'] = float(components.rstrip(' sec'))
            if line.startswith('Seeding time'):
                # Seeding time:			0.105874 sec		0.32414 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['fm_index_seed_time'] = float(components.rstrip(' sec'))
            if line.startswith('Filtering time'):
                # Filtering time:			3.68388 sec		11.2785 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['fm_index_filter_time'] = float(components.rstrip(' sec'))
            if line.startswith('Classification time'):
                # Classification time:		0.108888 sec		0.333369 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['fm_index_classification_time'] = float(components.rstrip(' sec'))
            if line.startswith('Ranking time'):
                # Ranking time:			0.312822 sec		0.957728 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['fm_index_rank_time'] = float(components.rstrip(' sec'))
            if line.startswith('Extension time'):
                # Extension time:			6.84071 sec		20.9434 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['fm_index_entension_time'] = float(components.rstrip(' sec'))
            if line.startswith('Sorting time'):
                # Sorting time:			1.16036 sec		3.55254 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['fm_index_sort_time'] = float(components.rstrip(' sec'))
            if line.startswith('Compaction time'):
                # Compaction time:			1.16036 sec		3.55254 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['fm_index_compact_time'] = float(components.rstrip(' sec'))
            if line.startswith('Alignment time'):
                # Alignment time:			1.7198 sec		5.26531 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['fm_index_alignment_time'] = float(components.rstrip(' sec'))
            if line.startswith('Output time'):
                # Output time:			2.38638 sec		7.30608 %
                components = line.split(':')[1].strip().split('\t')[0]
                result['fm_index_output_time'] = float(components.rstrip(' sec'))
            if line.startswith('Total reads'):
                # Total reads:			1048576
                components = line.split('\t')
                result['total_reads'] = int(float(components[3].strip()))
            if line.startswith('Mapped reads'):
                # Mapped reads:			1048576		100 %
                components = line.split('\t')
                result['mapped_reads'] = int(float(components[3].strip()))
            if line.startswith('Avg reads per bin'):
                # Avg reads per bin:		8192
                components = line.split('\t')
                result['avg_reads_per_bin'] = int(float(components[2].strip()))
    return result

if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument('yara_mapper_log_file', metavar='<yara mapper log file>', type=Path, help='The verbose stderr output of the yara mapper.')

    args = parser.parse_args()

    # print json file
    print(json.dumps(parse_yara_mapper_log(args.yara_mapper_log_file)))
