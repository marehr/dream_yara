
# ===================================
# simulate_genome.sh: generate reads - BEGIN
# ===================================

set (filter_ibf_bin_list "") # $bin_list unknown
foreach (bin_id RANGE ${filter_ibf_max_bin_id})
    # $(seq -f "$BIN_DIR/$BIN_NUMBER/bins/bin_%0${#BIN_NUMBER}g.fasta.gz" 0 1 $((BIN_NUMBER-1)))
    padded_number (padded_bin_id ${bin_id} ${filter_ibf_max_bin_id})
    list (APPEND filter_ibf_bin_list "${bin_dir}/bins/bin_${padded_bin_id}.fasta.gz")
endforeach ()
#
# # message (STATUS "filter_ibf_bin_list: ${filter_ibf_bin_list}")
#
add_custom_command (
    OUTPUT ${bin_dir}/reads_e${mapper_yara_read_errors}_${mapper_yara_read_length}.fastq
    DEPENDS ${filter_ibf_bin_list}
    WORKING_DIRECTORY "${bin_dir}"
    COMMAND ${CMAKE_COMMAND} -E make_directory ${bin_dir}/reads_e${mapper_yara_read_errors}_${mapper_yara_read_length}/
    COMMAND # reads_e$ERRORS\_$read_length
        generate_reads
            --seed ${simulate_seed}
            --output ${bin_dir}/reads_e${mapper_yara_read_errors}_${mapper_yara_read_length}
            --max_errors ${mapper_yara_read_errors}
            --number_of_reads ${mapper_yara_read_count}
            --read_length ${mapper_yara_read_length}
            --number_of_haplotypes ${simulate_haplotype_count}
            ${filter_ibf_bin_list}
    COMMAND ${CMAKE_COMMAND} -E echo "sha256sum -c reads_e${mapper_yara_read_errors}_${mapper_yara_read_length}.sha256"
    COMMAND sha256sum -c ${checksum_dir}/reads_e${mapper_yara_read_errors}_${mapper_yara_read_length}.sha256
    COMMAND ${CMAKE_COMMAND} -E cat ${bin_dir}/reads_e${mapper_yara_read_errors}_${mapper_yara_read_length}/*.fastq
            > "${bin_dir}/reads_e${mapper_yara_read_errors}_${mapper_yara_read_length}.fastq"
    COMMAND ${CMAKE_COMMAND} -E rm -rf ${bin_dir}/reads_e${mapper_yara_read_errors}_${mapper_yara_read_length}
)
#
# # give datasource a name
add_custom_target (
    dream_yara_read_data
    DEPENDS
        ${bin_dir}/reads_e${mapper_yara_read_errors}_${mapper_yara_read_length}.fastq
)
