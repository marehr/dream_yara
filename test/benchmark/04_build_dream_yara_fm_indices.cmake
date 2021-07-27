
# ===================================
# original_dream_yara.sh: build dream fm-indices - BEGIN
# ===================================

set (fm_indices "")
foreach (bin_id RANGE ${filter_ibf_max_bin_id})
    list (APPEND fm_index_bin${bin_id} "${bin_dir}/fm-indices/${bin_id}.lf.drp")
    list (APPEND fm_index_bin${bin_id} "${bin_dir}/fm-indices/${bin_id}.lf.drs")
    list (APPEND fm_index_bin${bin_id} "${bin_dir}/fm-indices/${bin_id}.lf.drv")
    list (APPEND fm_index_bin${bin_id} "${bin_dir}/fm-indices/${bin_id}.lf.pst")
    list (APPEND fm_index_bin${bin_id} "${bin_dir}/fm-indices/${bin_id}.rid.concat")
    list (APPEND fm_index_bin${bin_id} "${bin_dir}/fm-indices/${bin_id}.rid.limits")
    list (APPEND fm_index_bin${bin_id} "${bin_dir}/fm-indices/${bin_id}.sa.ind")
    list (APPEND fm_index_bin${bin_id} "${bin_dir}/fm-indices/${bin_id}.sa.len")
    list (APPEND fm_index_bin${bin_id} "${bin_dir}/fm-indices/${bin_id}.sa.val")
    list (APPEND fm_index_bin${bin_id} "${bin_dir}/fm-indices/${bin_id}.txt.concat")
    list (APPEND fm_index_bin${bin_id} "${bin_dir}/fm-indices/${bin_id}.txt.limits")
    list (APPEND fm_index_bin${bin_id} "${bin_dir}/fm-indices/${bin_id}.txt.size")
    list (APPEND fm_indices ${fm_index_bin${bin_id}})
endforeach ()

foreach (bin_id RANGE ${filter_ibf_max_bin_id})
    padded_number (padded_bin_id ${bin_id} ${filter_ibf_max_bin_id})
    # message (STATUS "padded_bin_id: ${padded_bin_id}")

    # set (tmp_dir "${bin_dir}/fm_indices/bin${bin_id}")
    set (tmp_prefix "${bin_dir}/fm-indices/tmp_bin${bin_id}__")

    if (NOT EXISTS "${checksum_dir}/fm-indices/fm_indices${padded_bin_id}.sha256")
        message (FATAL_ERROR "sha256 file '${checksum_dir}/fm-indices/fm_indices${padded_bin_id}.sha256' does not exists.")
    endif ()

    add_custom_command (
        OUTPUT ${fm_index_bin${bin_id}}
        DEPENDS ${bin_dir}/bins/bin_${padded_bin_id}.fasta.gz
        WORKING_DIRECTORY "${bin_dir}"
        COMMAND ${CMAKE_COMMAND} -E make_directory ${bin_dir}/fm-indices
        COMMAND
            dream_yara_indexer
                --output-prefix ${tmp_prefix} # trailing slash is needed
                --verbose
                --version-check 0
                ${bin_dir}/bins/bin_${padded_bin_id}.fasta.gz
        COMMAND ${CMAKE_COMMAND} -E echo "sha256sum -c fm-indices/fm_indices${padded_bin_id}.sha256"
        COMMAND sha256sum -c ${checksum_dir}/fm-indices/fm_indices${padded_bin_id}.sha256
        COMMAND ${CMAKE_COMMAND} -E rename ${tmp_prefix}0.lf.drp ${bin_dir}/fm-indices/${bin_id}.lf.drp
        COMMAND ${CMAKE_COMMAND} -E rename ${tmp_prefix}0.lf.drs ${bin_dir}/fm-indices/${bin_id}.lf.drs
        COMMAND ${CMAKE_COMMAND} -E rename ${tmp_prefix}0.lf.drv ${bin_dir}/fm-indices/${bin_id}.lf.drv
        COMMAND ${CMAKE_COMMAND} -E rename ${tmp_prefix}0.lf.pst ${bin_dir}/fm-indices/${bin_id}.lf.pst
        COMMAND ${CMAKE_COMMAND} -E rename ${tmp_prefix}0.rid.concat ${bin_dir}/fm-indices/${bin_id}.rid.concat
        COMMAND ${CMAKE_COMMAND} -E rename ${tmp_prefix}0.rid.limits ${bin_dir}/fm-indices/${bin_id}.rid.limits
        COMMAND ${CMAKE_COMMAND} -E rename ${tmp_prefix}0.sa.ind ${bin_dir}/fm-indices/${bin_id}.sa.ind
        COMMAND ${CMAKE_COMMAND} -E rename ${tmp_prefix}0.sa.len ${bin_dir}/fm-indices/${bin_id}.sa.len
        COMMAND ${CMAKE_COMMAND} -E rename ${tmp_prefix}0.sa.val ${bin_dir}/fm-indices/${bin_id}.sa.val
        COMMAND ${CMAKE_COMMAND} -E rename ${tmp_prefix}0.txt.concat ${bin_dir}/fm-indices/${bin_id}.txt.concat
        COMMAND ${CMAKE_COMMAND} -E rename ${tmp_prefix}0.txt.limits ${bin_dir}/fm-indices/${bin_id}.txt.limits
        COMMAND ${CMAKE_COMMAND} -E rename ${tmp_prefix}0.txt.size ${bin_dir}/fm-indices/${bin_id}.txt.size
    )
endforeach ()

# give datasource a name
add_custom_target (dream_yara_fm_indices_data DEPENDS ${fm_indices})
