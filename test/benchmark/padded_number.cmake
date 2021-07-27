function (padded_number out_number in_number max_number)
    string (LENGTH "${max_number}" max_length)
    string (LENGTH "${in_number}" in_length)
    math (EXPR length_diff "${max_length} - ${in_length}")

    set (return "${in_number}")
    foreach (i RANGE ${length_diff})
        if (NOT ${i} LESS ${length_diff})
            break ()
        endif ()

        set (return "0${return}")
    endforeach ()

    set ("${out_number}" "${return}" PARENT_SCOPE)
endfunction ()
