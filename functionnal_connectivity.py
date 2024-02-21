#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sidneykrystal and paulinefavre
"""

import os
from os.path import join
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nilearn import image as img
from nilearn import plotting
from nilearn.input_data import NiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure
from extract_Tian_atlas_rois import fetch_atlas_Tian_subparts



fsl_dir = './fsl'
input_dir = './input' #output of FMRIprep
output_dir = './output' #path where to write the results
atlas_dir = './atlas' #path where the Tian's atlas was downloaded
cases = [] #list of subjects to process in BIDS format


#Get the regions of interest for the amygldala FC analysis
atlas = fetch_atlas_Tian_subparts(atlas_dir,fsl_dir)
atlas_img = atlas['maps']
atlas_labels = atlas['labels']
atlas_descr = atlas['description']
del atlas_labels[0]
mask = img.load_img(atlas_img)

#Figure 1
plotting.plot_roi(atlas_img,
                  title=atlas_descr,
                  cmap='prism',
                  black_bg=True,
                  cut_coords=[-24, 15, -19],
                  draw_cross=False)

#Construct the masker from the atlas
masker = NiftiLabelsMasker(labels_img=mask,
                                  standardize=True,
                                  memory='nilearn_cache',
                                  verbose=1,
                                  detrend=True,
                                  low_pass = 0.08,
                                  high_pass = 0.009,
                                  t_r=2)

#Get the FC for all participants
all_rois = []
lAMY_rh = []
mAMY_rh = []
lAMY_lh = []
mAMY_lh = []

for case in cases:

    directory = output_dir + '/sub-'+case

    if not os.path.exists(directory):
        os.makedirs(directory)

#Get the confounds factors
    counfounds = input_dir + "/sub-"+case+"/ses-01/func/sub-"+case+"_ses-01_task-rest_run-1_desc-confounds_timeseries.tsv"
    counfounds_data=pd.read_table(counfounds)
    counfounds_data.fillna(0, inplace=True)
    #Write new file with selected confounding factors
    pd.DataFrame(counfounds_data[["csf","white_matter",
                                  "trans_x","trans_x_derivative1","trans_x_derivative1_power2","trans_x_power2",
                                  "trans_y","trans_y_derivative1","trans_y_derivative1_power2","trans_y_power2",
                                  "trans_z","trans_z_derivative1","trans_z_derivative1_power2","trans_z_power2",
                                  "rot_x","rot_x_derivative1","rot_x_derivative1_power2","rot_x_power2",
                                  "rot_y","rot_y_derivative1","rot_y_derivative1_power2","rot_y_power2",
                                  "rot_z","rot_z_derivative1","rot_z_derivative1_power2","rot_z_power2"]]).to_csv(directory+"/sub-"+case+"_task-rest_desc-selected_confounds_regressors.csv")

#Load preprocessed data
    rsfMRI_preproc = input_dir + '/sub-'+case+'/ses-01/func/sub-'+case+'_ses-01_task-rest_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz'

#Extract the timeseries
    time_series = masker.fit_transform(rsfMRI_preproc, confounds=directory+"/sub-"+case+"_task-rest_desc-selected_confounds_regressors.csv")

#Get the full functional connectivity matrix
    correlation_measure = ConnectivityMeasure(kind='correlation')

    full_matrix = correlation_measure.fit_transform([time_series])[0]
    np.fill_diagonal(full_matrix, 0)
    np.savetxt(directory+'/sub-'+case+'_full_matrix.csv', full_matrix)

    #Plot
    fig = plt.figure(figsize=(8,8))
    vmax = np.max(np.abs(full_matrix))
    title='Mean correlation' + ' atlas ' + atlas_descr
    plotting.plot_matrix(full_matrix,
                         vmin=-vmax, vmax=vmax,
                         cmap='RdBu_r',
                         title=title,
                         figure=fig,
                         colorbar=True,
                         labels=atlas_labels)
    plt.savefig(join(directory+'/sub-'+case+'_full_matrix.png'), bbox_inches='tight')

#Get the amygdala subnucleis' functional connectivity
    FC_lAMY_rh = full_matrix[2,:]
    lAMY_rh.append(FC_lAMY_rh)

    FC_mAMY_rh = full_matrix[3,:]
    mAMY_rh.append(FC_mAMY_rh)

    FC_lAMY_lh = full_matrix[8,:]
    lAMY_lh.append(FC_lAMY_lh)

    FC_mAMY_lh = full_matrix[9,:]
    mAMY_lh.append(FC_mAMY_lh)

#Save all subjects AMY FC as dataframes for subsequent group analyses
df_lAMY_rh = pd.DataFrame(lAMY_rh, index=cases, columns=atlas_labels)
df_lAMY_rh = df_lAMY_rh.set_index('sub-' + df_lAMY_rh.index.astype(str))
df_lAMY_rh.to_csv(output_dir+"/all_sub_lAMY_rh.csv")

df_mAMY_rh = pd.DataFrame(mAMY_rh, index=cases, columns=atlas_labels)
df_mAMY_rh = df_mAMY_rh.set_index('sub-' + df_mAMY_rh.index.astype(str))
df_mAMY_rh.to_csv(output_dir+"/all_sub_mAMY_rh.csv")

df_lAMY_lh = pd.DataFrame(lAMY_lh, index=cases, columns=atlas_labels)
df_lAMY_lh = df_lAMY_lh.set_index('sub-' + df_lAMY_lh.index.astype(str))
df_lAMY_lh.to_csv(output_dir+"/all_sub_lAMY_lh.csv")

df_mAMY_lh = pd.DataFrame(mAMY_lh, index=cases, columns=atlas_labels)
df_mAMY_lh = df_mAMY_lh.set_index('sub-' + df_mAMY_lh.index.astype(str))
df_mAMY_lh.to_csv(output_dir+"/all_sub_mAMY_lh.csv")
