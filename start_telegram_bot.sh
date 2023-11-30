#!/bin/bash
# wait 5 seconds
sleep 5
source /home/lunkwill/miniconda3/etc/profile.d/conda.sh  # Replace with the path to your conda.sh
conda activate base
python /home/lunkwill/projects/Lemmy_mod_tools/telegram_lunkstealth_bot.py
