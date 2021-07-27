# -----------------------------------------------------------------------------------------------------
# Copyright (c) 2006-2021, Knut Reinert & Freie Universität Berlin
# Copyright (c) 2016-2021, Knut Reinert & MPI für molekulare Genetik
# This file may be used, modified and/or redistributed under the terms of the 3-clause BSD-License
# shipped with this file and also available at: https://github.com/seqan/seqan3/blob/master/LICENSE.md
# -----------------------------------------------------------------------------------------------------

macro (require_mason)
    include(FetchContent)

    set (SEQAN_BUILD_SYSTEM "APP:mason2")
    FetchContent_Declare(
        seqan2_mason2
        GIT_REPOSITORY "https://github.com/seqan/seqan.git"
        GIT_TAG "develop"
        GIT_SHALLOW true
    )
    FetchContent_MakeAvailable(seqan2_mason2)
endmacro ()
