# Copyright (c) 2014 Paul Osborne. All rights reserved.
# This code is released as open sourrce under the terms of the
# MIT License v2.0 (http://opensource.org/licenses/MIT)
#
# -------------------------------------------------------------
#
# This script is designed to be *sourced* and not to be run
# directly.  In fact, running it directly is unlikely to
# do much of anything.

DNAV_DIRECTORY=$(readlink -f $(dirname "${BASH_SOURCE[0]}"))

dnav() {
    output=$(python $DNAV_DIRECTORY/dnav.py $*)
    retval="$?"

    # A status of 1 indicates that the program would like us
    # to change to the provided directory
    if [ $retval -eq 1 ]; then
        cd $output
        return 0
        # less than 0 indicates an error or other status from
        # the program that does not require us to modify anything
    elif [ $retval -lt 0 ]; then
        echo $output
        return $retval
    else
        echo $output
        return $retval
    fi
}
