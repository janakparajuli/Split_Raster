# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 21:18:52 2021

@author: janak
"""

import rasterio
import os
from glob import glob
import numpy as np

in_folder=r"E:/THESIS/Scripts/Janak_20201026/data/GLabel/"
out_folder=r'E:/THESIS/Scripts/Janak_20201026/data/Splitted_GLabel/'

tiffs=glob(in_folder+'*.tif')
for tiff in tiffs:
    print(tiff)
    img=rasterio.open(tiff)
    img_name=img.name.split('/')[-1].split('_')[0][:6]
    img_transform=img.transform
    img_crs=img.crs
    
    print('Reading image {} ...'.format(img_name))
    img_array=img.read().astype('uint16')
    
    #Decide how many splits you need and split accordingly
    S = 21
    M = img_array.shape[1]//S
    N = img_array.shape[2]//S
    bounds=list()
    transforms = list()
    
    print('Splitting image {} ...'.format(img_name))
    tiles = [img_array[:,x:x+M,y:y+N] for x in range(0,img_array.shape[1],M) for y in range(0,img_array.shape[2],N)]
    bounds = [[img_transform[2]+y*10,img_transform[5]-M*10-x*10,img_transform[2]+N*10+y*10,img_transform[5]-x*10] for x in range(0,img_array.shape[1],M) for y in range(0,img_array.shape[2],N)]
    transforms=[rasterio.transform.from_bounds(bounds[i][0],bounds[i][1],bounds[i][2],bounds[i][3],N,M) for i in range(len(tiles))]

    for i in range(len(tiles)):
        print('---Writing Tile {}'.format(i))
        with rasterio.open(os.path.join(out_folder,img_name+'_Clip_{}.tif'.format(i)),
                  'w',
                  driver='GTiff',
                  height=tiles[i].shape[1],
                  width=tiles[i].shape[2],
                  count=img.count,
                  dtype='uint16',
                  crs=img_crs,
                  transform=transforms[i],) as f:
            f.write(tiles[i])
        print('---Writing tile {} completed...'.format(i))
    print('Image {} is splitted...'.format(img_name))
            
del in_folder, out_folder, img, img_transform, img_name, img_array, bounds, transforms

#Check for and delete none valued label data
in_folder=r'E:/THESIS/Scripts/Janak_20201026/data/Splitted_GLabel/'

label_tiffs=glob(in_folder+'*.tif')
lbl_img_names=list()

for label_tiff in label_tiffs:
    lbl_img=rasterio.open(label_tiff)
    lbl_img_name=lbl_img.name.split('/')[-1]
    lbl_array=lbl_img.read().astype('uint16')
    unique,count = np.unique(lbl_array,return_counts=True)
    if len(unique)==1 and unique == 65535: # and tiff=='E:/THESIS/Scripts/Janak_20201026/data/Splitted_GLabel\\T44RQR_Clip_99.tif':
        lbl_img.close()
        print('Tile {} is being deleted...'.format(lbl_img_name))
        lbl_img_names.append(lbl_img_name)
        os.remove(label_tiff)
del in_folder, label_tiffs

in_folder=r'E:/THESIS/Scripts/Janak_20201026/data/Splitted_FTiff_DEM/'
image_tiffs=glob(in_folder+'*.tif')
# count=0

for image_tiff in image_tiffs:
    image_name=image_tiff.split('\\')[-1]
    if image_name in lbl_img_names:
        print('Deleting unwanted tile {}'.format(image_name))
        # count+=1
        os.remove(image_tiff)







