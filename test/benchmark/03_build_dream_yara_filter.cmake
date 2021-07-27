
# ===================================
# original_dream_yara.sh: build dream filter (IBF) - BEGIN
# ===================================

set (filter_ibf_bin_list "") # $bin_list unknown
foreach (bin_id RANGE ${filter_ibf_max_bin_id})
    # $(seq -f "$BIN_DIR/$BIN_NUMBER/bins/bin_%0${#BIN_NUMBER}g.fasta.gz" 0 1 $((BIN_NUMBER-1)))
    padded_number (padded_bin_id ${bin_id} ${filter_ibf_max_bin_id})
    list (APPEND filter_ibf_bin_list "${bin_dir}/bins/bin_${padded_bin_id}.fasta.gz")
endforeach ()

# message (STATUS "filter_ibf_bin_list: ${filter_ibf_bin_list}")

add_custom_command (
    OUTPUT ${filter_ibf_filename}
    DEPENDS ${filter_ibf_bin_list}
    WORKING_DIRECTORY "${bin_dir}"
    COMMAND
        dream_yara_build_filter
            --output-file ${filter_ibf_filename}
            --kmer-size ${filter_ibf_kmer_size}
            --bloom-size ${filter_ibf_bloom_size}
            --threads ${filter_ibf_threads}
            --num-hash ${filter_ibf_num_hash}
            --verbose
            --version-check 0
            ${filter_ibf_bin_list}
    COMMAND ${CMAKE_COMMAND} -E echo "sha256sum -c 19_1G.filter.sha256"
    COMMAND sha256sum -c ${checksum_dir}/19_1G.filter.sha256
)

# give datasource a name
add_custom_target (dream_yara_filter_data DEPENDS ${filter_ibf_filename})
