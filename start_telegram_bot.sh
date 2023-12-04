#!/bin/bash
# wait 5 seconds
sleep 5
source /home/lunkwill/miniconda3/etc/profile.d/conda.sh  # Replace with the path to your conda.sh
conda activate base
cd /home/lunkwill/projects/Lemmy_mod_tools
python /home/lunkwill/projects/Lemmy_mod_tools/main.py # > ~/startup_log.txt 2>&1
