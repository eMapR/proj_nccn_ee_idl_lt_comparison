# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 14:40:06 2017

@author: braatenj
"""

import subprocess
import sys

tileListFile = sys.argv[1]
vrtPath = sys.argv[2]

cmd = 'gdalbuildvrt -tap -tr 30 30 -srcnodata 0 -input_file_list '+tileListFile+' '+vrtPath
subprocess.call(cmd, shell=True)