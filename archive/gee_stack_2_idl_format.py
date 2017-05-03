

import sys
import os
import subprocess
import multiprocessing


def gdal_translate(cmd):
  print(cmd)
  return subprocess.call(cmd, shell=True)




# get the arguments
eeStack = sys.argv[1]   #'/vol/v1/general_files/user_files/justin/for_others/fs_karen/data/landtrendr/ycd_test/'
outDir = sys.argv[2]  #'/vol/v1/general_files/user_files/justin/for_others/fs_karen/data/landtrendr/ycd_test/'
name = sys.argv[3]    #'fs_karen_ycd_test_'
indexID = sys.argv[4] #'nbr'
nVert = int(sys.argv[5])
startYear = int(sys.argv[6])
endYear = int(sys.argv[7])
proj = sys.argv[8]    #'EPSG:5070'
delete = sys.argv[9]  #True

#eeStack = '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/lewi/corrected_nbr_15_offset_normal/nccn_lewi_gee_vs_idl_all_stack_normal.tif'   #'/vol/v1/general_files/user_files/justin/for_others/fs_karen/data/landtrendr/ycd_test/'
#outDir = '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/lewi/corrected_nbr_15_offset_normal'  #'/vol/v1/general_files/user_files/justin/for_others/fs_karen/data/landtrendr/ycd_test/'
#name = 'test'    #'fs_karen_ycd_test_'
#indexID = 'nbr'
#nVert = 7
#startYear = 1984
#endYear = 2012
#proj = 'EPSG:5070'
#delete = 'keep'



# get the arguments
#indir = '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/lewi'   #'/vol/v1/general_files/user_files/justin/for_others/fs_karen/data/landtrendr/ycd_test/'
#outdir = '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/lewi'  #'/vol/v1/general_files/user_files/justin/for_others/fs_karen/data/landtrendr/ycd_test/'
#name = 'nccn_lewi_gee_vs_idl'    #'fs_karen_ycd_test_'
#indexID = 'nbr' #'nbr'
#proj = 'EPSG:5070'    #'EPSG:5070'
#delete = False  #True


if outDir[-1] != '/':
  outDir += '/'
if name[-1] != '_':
  name += '_'


# define the list of replacement types in the new out images    
outTypes = ['vert_yrs.bsq',
            'vert_src.bsq',
            'vert_fit.bsq',
            'ftv_'+indexID+'.bsq',            
            'ftv_tcb.bsq',
            'ftv_tcg.bsq',
            'ftv_tcw.bsq']

vertStops = []
for vertType in range(4):  
  vertStops.append(vertType*nVert+1)

nYears = (endYear - startYear) + 1
ftvStops = []  
for ftvType in range(1,5):  
  ftvStops.append(ftvType*nYears+vertStops[-1])
  
bandStops = vertStops+ftvStops
bandRanges = [range(bandStops[i],bandStops[i+1]) for i in range(len(bandStops)-1)]


# get the in tifs and define the out bsqs           
outFiles = [outDir+name+outType for outType in outTypes]

# make a list of translate cmds to translate tifs to bsq
cmds = []
for i in range(len(outFiles)):
  bands = ' -b '+' -b '.join([str(band) for band in bandRanges[i]])
  cmds.append('gdal_translate -q --config GDAL_DATA "/usr/lib/anaconda/share/gdal" -of ENVI -a_srs ' + proj + bands + ' ' + eeStack + ' ' + outFiles[i])

# loop through the files
pool = multiprocessing.Pool(processes=len(cmds))
pool.map(gdal_translate, cmds)  
pool.close()

# delete the original tif file is requested
if delete =='delete':
  os.remove(eeStack)


