# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 16:39:03 2017

@author: braatenj
"""

import subprocess

eeVert = '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/noca/label_v01/nccn_gee_vs_idl_noca_greatest_fast_disturbance_mmu11_tight_nodata.bsq'
clipFile = '/vol/v1/proj/nccn/gee_idl_lt_compare/vector/LPa01_LEWI_MORA_NOCA_OLYM.geojson'


cmd = 'gdal_rasterize -i -burn -9999 ' +clipFile+' '+eeVert
subprocess.call(cmd, shell=True)

