#!/bin/bash

# Author: Pauline Favre <pauline@favre-univ.fr>
#
# fMRIPrep version: 20.2.1
#
# Usage: ./fmri_preprocessing.sh <BIDS number>

echo "BIDS number: $1"
/usr/local/miniconda/bin/fmriprep /data /out participant --nthreads 1 --omp-nthreads 50 --use-aroma --use-syn-sdc --fs-no-reconall --participant_label sub-$1