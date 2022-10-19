# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 15:36:41 2022

@author: User
"""

import constants as c
import pandas as pd
import file_manager as fm
import processing as pross

def prepare_test_dfs(df, window_size, density, local):
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_dens' + str(density) + '_loc' + str(local)
    dataset = fm.PREPARATION_DIR + '\\' + dir_name
    fm.do_dir(dataset)
    
    #select time windows
    df = df[df['time'] % window_ms == 0]

    #select electrodes
    electrodes = c.DENSITY[density]
    
    if local:
        electrodes = list(set(electrodes) & set(c.CHANNELS_VISUAL))
    
    df = df[df['channel'].isin(electrodes)] #shallow copy protection

    #split by test condition
    for cond in c.TEST_CONDITIONS:
        columns = ['part','time','channel', cond]
        cond_df = df[columns]
        
        #save
        dataframe_file = dataset + '\\' + cond + '.csv'
        cond_df.to_csv(dataframe_file, index = False)
    
def load_test_dfs(window_size, density, local):
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_dens' + str(density) + '_loc' + str(local)
    dataset = fm.PREPARATION_DIR + '\\' + dir_name
    
    loaded = {}
    
    for cond in c.TEST_CONDITIONS:
        dataframe_file = dataset + '\\' + cond + '.csv'
        prepared = pd.read_csv(dataframe_file)
        
        loaded[cond] = prepared
        
    return loaded
    
def prepare():
    dataset = fm.PREPARATION_DIR 
    fm.do_dir(dataset)
    
    df = pross.load_evo_df()
        
    #select post stimulus time interval 0 to 500
    df = df[(df['time'] >= c.TEST_INTERVAL_MIN) & 
            (df['time'] <= c.TEST_INTERVAL_MAX)]
    
    #format wide
    df = df.pivot(index=['part','time','channel'], 
                                    columns='condition', 
                                    values='value')
    
    #calcualte difference between conditions into new column
    df[c.LATERALIZATION] = df['vs_right'] - df['vs_left']
    
    df = df.reset_index()

    #prepare cond dfs
    for w in c.WINDOW_SIZE:
        for d in c.DENSITY.keys():
            for l in c.LOCAL:
                prepare_test_dfs(df, w, d, l)
        
        
        
        
        
        
        
    
    
    
    




