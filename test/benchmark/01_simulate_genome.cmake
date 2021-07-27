
# ===================================
# simulate.sh: simulate genome - BEGIN
# ===================================

include (../cmake/require_mason.cmake)

require_mason ()

# BINARY_DIR="./bin"
# OUT_DIR="./output"
# LENGTH=536870912 # 0.5 * 2^30 = 512MB # 4*2^30 =  4GiB
# SEED=42 # was 20181406 before, but was hardcoded to 42 in seqan
# BIN_NUMBER=128
# ERRORS=2
# READ_LENGTHS="100 150 250"
# READ_COUNT=1048576 # 2^20 = 1MB
# HAPLOTYPE_COUNT=16

set (simulate_genome_split_bin_list "")
foreach (bin_id RANGE ${filter_ibf_max_bin_id})
    padded_number (padded_bin_id ${bin_id} ${filter_ibf_max_bin_id})
    list (APPEND simulate_genome_split_bin_list "${bin_dir}/genome_split/bin_${padded_bin_id}.fasta")
endforeach ()

add_custom_command (
    OUTPUT ${simulate_genome_split_bin_list}
    WORKING_DIRECTORY "${bin_dir}"
    COMMENT "Simulating ${filter_ibf_bin_number} bins with reference length of ${simulate_genome_length} and bin_length of ${filter_ibf_bin_length}"

    COMMAND ${CMAKE_COMMAND} -E echo "Simulating genome"
    COMMAND mason_genome -l ${simulate_genome_length} -o ${bin_dir}/reference.fasta -s ${simulate_seed}
    COMMAND ${CMAKE_COMMAND} -E echo "sha256sum -c reference.fasta.sha256"
    COMMAND sha256sum -c ${checksum_dir}/reference.fasta.sha256
    COMMAND ${CMAKE_COMMAND} -E make_directory ${bin_dir}/genome_split/
    COMMAND ${CMAKE_COMMAND} -E echo "Splitting genome into bins"
    COMMAND
        split_sequence
            --input ${bin_dir}/reference.fasta
            --length ${filter_ibf_bin_length}
            --parts ${filter_ibf_bin_number}
            --output ${bin_dir}/genome_split/
    COMMAND ${CMAKE_COMMAND} -E echo "sha256sum -c genome_split.sha256"
    COMMAND sha256sum -c ${checksum_dir}/genome_split.sha256
    COMMAND rm ${bin_dir}/reference.fasta
)

set (simulate_bin_list "")
foreach (bin_id RANGE ${filter_ibf_max_bin_id})
    padded_number (padded_bin_id ${bin_id} ${filter_ibf_max_bin_id})
    list (APPEND simulate_bin_list "${bin_dir}/bins/bin_${padded_bin_id}.fasta.gz")

    add_custom_command (
        OUTPUT ${bin_dir}/bins/bin_${padded_bin_id}.fasta.gz
               ${bin_dir}/info/bin_${padded_bin_id}.vcf
        DEPENDS ${bin_dir}/genome_split/bin_${padded_bin_id}.fasta
        WORKING_DIRECTORY "${bin_dir}"
        COMMAND ${CMAKE_COMMAND} -E make_directory ${bin_dir}/bins/
        COMMAND ${CMAKE_COMMAND} -E make_directory ${bin_dir}/info/
        COMMAND
            mason_variator
                -ir ./genome_split/bin_${padded_bin_id}.fasta
                -n ${simulate_haplotype_count}
                -of ./bins/bin_${padded_bin_id}.fasta
                -ov ./info/bin_${padded_bin_id}.vcf
        COMMAND ${CMAKE_COMMAND} -E echo "sha256sum -c bins/bin_${padded_bin_id}.fasta.sha256"
        COMMAND sha256sum -c ${checksum_dir}/bins/bin_${padded_bin_id}.fasta.sha256
        COMMAND ${CMAKE_COMMAND} -E echo "sha256sum -c info/bin_${padded_bin_id}.vcf.sha256"
        COMMAND sha256sum -c ${checksum_dir}/info/bin_${padded_bin_id}.vcf.sha256
        COMMAND gzip ./bins/bin_${padded_bin_id}.fasta
    )
endforeach ()

# give datasource a name
add_custom_target (dream_yara_genome_data DEPENDS ${simulate_bin_list})
