import numpy as np
import os
import sys
sys.path.append('../')
import config
import matplotlib.pyplot as plt
import data as d
from pathlib import Path
from features import feature_removal as fr

def metric_1(data:np.ndarray, channels=range(8)):
    """ 
        This function calculates theta/beta ratio for given data.
        The data has to be of shape, (epochs, channels. bands)
    """

    theta_idx = 1
    beta_idx = 3

    out = data[:,channels,theta_idx] / data[:,channels,beta_idx]

    return out

def plot_metric(data:np.ndarray, channels=range(8)):
    """ the shape of data should be (epochs, channels) """

    fig, ax = plt.subplots(figsize=(10,10)) 
    for i in channels:
        ax.plot(data[:,i].reshape(-1),label=f'channel: {i}')
        
    ax.legend()
    plt.show()

def get_attention_metric(file_name:str):
    """ This function calculates attention_metric based on the given filename or folder """

    """
        Inputs: file_name is a string. It can be either a file_name or name of the folder, incase which
        all the data inside that folder will be vstacked
        
        Outpus: Attention_metric
    """
    
    path = Path(file_name)

    if(os.path.isfile(path)):
        data = d.load_pickle_file(path)
    elif os.path.isdir(path):
        data = d.load_all_pickle_files(path,vstack=True)
    else:
        print(f"The path {path} does not exist")

    clean_data = d.clean_data(data,channels=range(8),threshold_fn=fr.max_amplitude)
    print(f"Clean data shape:{clean_data.shape}")

    _bandpower = d.epoch_bandpower(clean_data,per_epoch=1, channels=range(8),relative=False)

    _metrics = d.metric_1(_bandpower)

    return _metrics


