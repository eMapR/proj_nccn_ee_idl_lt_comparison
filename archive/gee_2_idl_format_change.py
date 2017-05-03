

import sys
import os
import glob
import subprocess
import multiprocessing


def gdal_translate(cmd):
  print(cmd)
  return subprocess.call(cmd, shell=True)




# get the arguments
indir = sys.argv[1]   #'/vol/v1/general_files/user_files/justin/for_others/fs_karen/data/landtrendr/ycd_test/'
outdir = sys.argv[2]  #'/vol/v1/general_files/user_files/justin/for_others/fs_karen/data/landtrendr/ycd_test/'
name = sys.argv[3]    #'fs_karen_ycd_test_'
indexID = sys.argv[4] #'nbr'
proj = sys.argv[5]    #'EPSG:5070'
delete = sys.argv[6]  #True


# get the arguments
#indir = '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/lewi'   #'/vol/v1/general_files/user_files/justin/for_others/fs_karen/data/landtrendr/ycd_test/'
#outdir = '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/lewi'  #'/vol/v1/general_files/user_files/justin/for_others/fs_karen/data/landtrendr/ycd_test/'
#name = 'nccn_lewi_gee_vs_idl'    #'fs_karen_ycd_test_'
#indexID = 'nbr' #'nbr'
#proj = 'EPSG:5070'    #'EPSG:5070'
#delete = False  #True




# make sure the paths have final slash
if indir[-1] != '/':
  indir += '/'
if outdir[-1] != '/':
  outdir += '/'
if name[-1] != '_':
  name += '_'

# create the core basename
outcore = indir + name

# define the list of image type to search for
intypes = ['vert_year.tif',
           'vert_val.tif',
           'ftv_tcb.tif',
           'ftv_tcg.tif',
           'ftv_tcw.tif',
           'ftv_index.tif']

# define the list of replacement types in the new out images    
outtypes = ['vert_yrs.bsq',
            'vert_vals.bsq',
            'ftv_tcb.bsq',
            'ftv_tcg.bsq',
            'ftv_tcw.bsq',
            'ftv_'+indexID+'.bsq']

# get the in tifs and define the out bsqs  
infiles = [glob.glob(indir+'*'+intype)[0] for intype in intypes]          
outfiles = [infiles[i].replace(intypes[i],outtypes[i]) for i in range(len(intypes))]

# make a list of translate cmds to translate tifs to bsq
cmds = []
for i in range(len(infiles)):
  cmds.append('gdal_translate -q --config GDAL_DATA "/usr/lib/anaconda/share/gdal" -of ENVI -a_srs ' + proj + ' ' + infiles[i] + ' ' + outfiles[i])

# loop through the files
pool = multiprocessing.Pool(processes=len(cmds))
pool.map(gdal_translate, cmds)  
pool.close()

# delete the original tif file is requested
if delete =='delete':
  for fn in infiles:
    os.remove(fn)


