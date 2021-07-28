
set (bin_dir "${CMAKE_CURRENT_BINARY_DIR}/data/benchmark1") # BIN_DIR
# set (benchmark_dir "${bin_dir}") # BENCHMARK_DIR
# set (fm_indices_dir "${bin_dir}/fm-indices")
# set (simulate_genome_filedir "${bin_dir}")
set (checksum_dir "${CMAKE_SOURCE_DIR}/test/data/benchmark1")

set (simulate_genome_length "536870912") # 512Mb; LENGTH (4*2^30)
set (simulate_haplotype_count "16") # HAPLOTYPE_COUNT (16)
set (simulate_seed "42") # 512Mb; LENGTH (4*2^30)

# The number of bins; How many bins to create.
set (filter_ibf_bin_number 128) # $BIN_NUMBER (128) unknown UNUSED
math (EXPR filter_ibf_bin_length "${simulate_genome_length} / ${filter_ibf_bin_number}") # $bin_length ($LENGTH / $BIN_NUMBER)

set (mapper_yara_read_length 100) # $READ_LENGTH (100, 250) unknown UNUSED
set (mapper_yara_read_errors 2) # $ERRORS (2) unknown UNUSED
set (mapper_yara_read_count 1048576) # $ERRORS (1048576) # 2^20 = 1MB

# used by build_dream_yara_filter - START
set (filter_ibf_kmer_size 19) # $K (19, 23, 31) unknown
set (filter_ibf_bloom_size 1) # $SIZE (16, 8) unknown

include(ProcessorCount)
ProcessorCount(NCPU)
set (filter_ibf_threads 1) # $THREADS (32) unknown
if(NCPU GREATER 1)
    set (filter_ibf_threads "${NCPU}") # $THREADS (32) unknown
endif()
set (filter_ibf_num_hash 2) # $HASH (2) unknown
# e.g. <BENCHMARK_DIR>/128/19_16G.filter
set (filter_ibf_filename "${bin_dir}/${filter_ibf_kmer_size}_${filter_ibf_bloom_size}G.filter") # $ibf_filename unknown
# used by build_dream_yara_filter - END

# derived variables:
math (EXPR filter_ibf_max_bin_id "${filter_ibf_bin_number} - 1") # needed for foreach

add_executable (split_sequence split_sequence.cpp)
target_link_libraries (split_sequence PUBLIC seqan3::seqan3)

add_executable (generate_reads generate_reads.cpp)
target_link_libraries (generate_reads PUBLIC seqan3::seqan3)

include (padded_number.cmake)

file (MAKE_DIRECTORY "${bin_dir}")

include (01_simulate_genome.cmake)
include (02_generate_reads.cmake)
include (03_build_dream_yara_filter.cmake)
include (04_build_dream_yara_fm_indices.cmake)

enable_testing ()

set (benchmark_util_dir "${CMAKE_CURRENT_SOURCE_DIR}/util")
set (benchmark_dir "${bin_dir}")

add_custom_target (benchmark1 DEPENDS dream_yara_mapper)

add_custom_target (benchmark1_data
    DEPENDS
        dream_yara_read_data
        dream_yara_fm_indices_data
        dream_yara_filter_data)

add_test(
    NAME benchmark1_benchmark
    COMMAND
        ${benchmark_util_dir}/execute_dream_yara_mapper_benchmark_and_add_csv_entry.sh
        "${benchmark_util_dir}"
        "$<TARGET_FILE_DIR:dream_yara_mapper>"
        "${benchmark_dir}"
        "${benchmark_dir}"
)
