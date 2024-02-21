#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: paulinefavre
"""
import subprocess
import os
from sklearn.utils import Bunch

os.environ["FSLOUTPUTTYPE"] = "NIFTI_GZ" #Fix the bug with subprocess.call


#Function to fetch the newly built atlas
def fetch_atlas_Tian_subparts(atlas_dir, fsl_dir):

    atlas=os.path.join(atlas_dir,'3T/Subcortex-Only','Tian_Subcortex_S2_3T_2009cAsym.nii.gz')

    #Extract Regions of Interest (ROIs) from Tian's atlas

    subdirectory=os.path.join(atlas_dir,'Tian_S2_3T_subparts/')
    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)

    if not os.path.exists(subdirectory + 'ROIs_Tian_S2.nii.gz'):
        #AMY_R lat intensity = 3     #NOTE:Regions were visually inspected with fsleyes to obtain their given intesities
        cmd = fsl_dir + '/bin/fslmaths ' + atlas + ' -thr ' + str(2.9) + ' -uthr ' + str(3.1) + ' -add ' + str(3) + ' ' + subdirectory + 'AMY_R_lat_Tian.nii.gz'
        subprocess.call(cmd, shell=True)

        #AMY_R med intensity = 4
        cmd = fsl_dir + '/bin/fslmaths ' + atlas + ' -thr ' + str(3.9) + ' -uthr ' + str(4.1) + ' -add ' + str(4) + ' ' + subdirectory + 'AMY_R_med_Tian.nii.gz'
        subprocess.call(cmd, shell=True)

        #AMY_L lat intensity = 19
        cmd = fsl_dir + '/bin/fslmaths ' + atlas + ' -thr ' + str(18.9) + ' -uthr ' + str(19.1) + ' -add ' + str(19) + ' ' + subdirectory + 'AMY_L_lat_Tian.nii.gz'
        subprocess.call(cmd, shell=True)

        #AMY_L med intensity = 20
        cmd = fsl_dir + '/bin/fslmaths ' + atlas + ' -thr ' + str(19.9) + ' -uthr ' + str(20.1) +  ' -add ' + str(20) + ' ' + subdirectory + 'AMY_L_med_Tian.nii.gz'
        subprocess.call(cmd, shell=True)

        #HIP_R ant intensity = 1
        cmd = fsl_dir + '/bin/fslmaths ' + atlas + ' -thr ' + str(0.9) + ' -uthr ' + str(1.1) +  ' -add ' + str(1) + ' ' + subdirectory + 'HIP_R_ant_Tian.nii.gz'
        subprocess.call(cmd, shell=True)

        #HIP_R post intensity = 2
        cmd = fsl_dir + '/bin/fslmaths ' + atlas + ' -thr ' + str(1.9) + ' -uthr ' + str(2.1) +  ' -add ' + str(2) + ' ' + subdirectory + 'HIP_R_post_Tian.nii.gz'
        subprocess.call(cmd, shell=True)

        #HIP_L ant intensity = 17
        cmd = fsl_dir + '/bin/fslmaths ' + atlas + ' -thr ' + str(16.9) + ' -uthr ' + str(17.1) +  ' -add ' + str(17) + ' ' + subdirectory + 'HIP_L_ant_Tian.nii.gz'
        subprocess.call(cmd, shell=True)

        #HIP_L post intensity = 18
        cmd = fsl_dir + '/bin/fslmaths ' + atlas + ' -thr ' + str(17.9) + ' -uthr ' + str(18.1) +  ' -add ' + str(18) + ' ' + subdirectory + 'HIP_L_post_Tian.nii.gz'
        subprocess.call(cmd, shell=True)

        #NAc_R shell = 9
        cmd = fsl_dir + '/bin/fslmaths ' + atlas + ' -thr ' + str(8.9) + ' -uthr ' + str(9.1) +  ' -add ' + str(9) + ' ' + subdirectory + 'NAc_R_shell_Tian.nii.gz'
        subprocess.call(cmd, shell=True)

        #NAc_R core = 10
        cmd = fsl_dir + '/bin/fslmaths ' + atlas + ' -thr ' + str(9.9) + ' -uthr ' + str(10.1) +  ' -add ' + str(10) + ' ' + subdirectory + 'NAc_R_core_Tian.nii.gz'
        subprocess.call(cmd, shell=True)

        #NAc_L shell = 25
        cmd = fsl_dir + '/bin/fslmaths ' + atlas + ' -thr ' + str(24.9) + ' -uthr ' + str(25.1) +  ' -add ' + str(25) + ' ' + subdirectory + 'NAc_L_shell_Tian.nii.gz'
        subprocess.call(cmd, shell=True)

        #NAc_R core = 26
        cmd = fsl_dir + '/bin/fslmaths ' + atlas + ' -thr ' + str(25.9) + ' -uthr ' + str(26.1) +  ' -add ' + str(26) + ' ' + subdirectory + 'NAc_L_core_Tian.nii.gz'
        subprocess.call(cmd, shell=True)


        #Put all ROIs together in one mask
        subprocess.call('cp ' + subdirectory + 'AMY_R_lat_Tian.nii.gz ' + subdirectory + 'ROIs_Tian_S2.nii.gz',shell=True)
        subprocess.call(fsl_dir + '/bin/fslmaths ' + subdirectory + 'ROIs_Tian_S2.nii.gz' + ' -add ' +
                                subdirectory + 'AMY_R_med_Tian.nii.gz' + ' -add ' +
                                subdirectory + 'AMY_L_lat_Tian.nii.gz' + ' -add ' +
                                subdirectory + 'AMY_L_med_Tian.nii.gz' + ' -add ' +
                                subdirectory + 'HIP_R_ant_Tian.nii.gz' + ' -add ' +
                                subdirectory + 'HIP_L_ant_Tian.nii.gz' + ' -add ' +
                                subdirectory + 'HIP_R_post_Tian.nii.gz' + ' -add ' +
                                subdirectory + 'HIP_L_post_Tian.nii.gz' + ' -add ' +
                                subdirectory + 'NAc_R_shell_Tian.nii.gz' + ' -add ' +
                                subdirectory + 'NAc_L_shell_Tian.nii.gz' + ' -add ' +
                                subdirectory + 'NAc_R_core_Tian.nii.gz' + ' -add ' +
                                subdirectory + 'NAc_L_core_Tian.nii.gz' +
                                ' ' + subdirectory + 'ROIs_Tian_S2.nii.gz',shell=True)


        #Remove background
        cmd = fsl_dir + '/bin/fslmaths ' + subdirectory + 'ROIs_Tian_S2.nii.gz' + ' -sub ' + str(154) + ' ' + subdirectory + "ROIs_Tian_S2.nii.gz"
        subprocess.call(cmd, shell=True)


    #Write labels together with the atlas
    labels='''0	NONE
    1	HIP_R_ant
    2	HIP_R_post
    3	AMY_R_lat
    4	AMY_R_med
    9	NAc_R_shell
    10	NAc_R_core
    17	HIP_L_ant
    18	HIP_L_post
    19	AMY_L_lat
    20	AMY_L_med
    25	NAc_L_shell
    26	NAc_L_core'''

    if not os.path.exists(subdirectory+'ROIs_Tian_S2_labels.txt'):
        with open(subdirectory+'ROIs_Tian_S2_labels.txt', 'x') as f:
            f.write(labels)

    #Return atlas parameters
    fdescr = "Tian's atlas subparts"
    labels_img = subdirectory+"ROIs_Tian_S2_labels.txt"
    atlas_img = subdirectory+"ROIs_Tian_S2.nii.gz"
    labels = []
    indices = []
    with open(labels_img, "r") as fp:
        for line in fp.readlines():
            index, label = line.strip().split('\t')
            indices.append(index)
            labels.append(label)
    params = {'description': fdescr, 'maps': atlas_img,
                  'labels': labels, 'indices': indices}
    return Bunch(**params)
