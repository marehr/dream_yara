#!/usr/bin/env bash

if [ "$#" -lt 4 ]; then
    echo "$0 <BENCHMARK_UTIL_DIR> <BINARY_DIR> <TMP_DIR> <BENCHMARK_DIR>"
    exit 1
fi

set -e
set -x

BENCHMARK_UTIL_DIR="$1"
BINARY_DIR="$2"
TMP_DIR="$3"
BENCHMARK_DIR="$4"
python3=$(command -v python3)

threads=4
error_rate=0.03 # 0$(bc -l <<< "($ERRORS+1)/$READ_LENGTH")

/usr/bin/time -o "$TMP_DIR/yara_mapper.time" -v \
    $BINARY_DIR/dream_yara_mapper \
        --bloom-filter $BENCHMARK_DIR/19_1G.filter \
        --output-file $BENCHMARK_DIR/19_1G_100.sam \
        --threads $threads \
        --error-rate $error_rate \
        --verbose \
        --version-check 0 \
        $BENCHMARK_DIR/fm-indices/ \
        $BENCHMARK_DIR/reads_e2_100.fastq \
        &> $TMP_DIR/yara_mapper.log

$python3 $BENCHMARK_UTIL_DIR/parse_time_log.py $TMP_DIR/yara_mapper.time > $TMP_DIR/yara_mapper.time.json
$python3 $BENCHMARK_UTIL_DIR/parse_yara_mapper_log.py $TMP_DIR/yara_mapper.log > $TMP_DIR/yara_mapper.log.json

$python3 $BENCHMARK_UTIL_DIR/add_benchmark_csv_entry.py \
    $TMP_DIR/yara_mapper.time.json \
    $TMP_DIR/yara_mapper.log.json \
    --append-to-csv $BENCHMARK_DIR/benchmark_csv_file.csv
