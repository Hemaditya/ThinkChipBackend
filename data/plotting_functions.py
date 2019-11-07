import matplotlib.pyplot as plt
import math

def compare_metrics(*args, labels=[],channels=range(8)):
    '''
        This function will plot the metrics of different data given as arguments.
    '''

    w, h = len(channels)*7, len(channels)*8
    nrows = math.ceil(len(channels)//2)
    ncols = 2
    fig, ax = plt.subplots(nrows, ncols, figsize=(w,h))
    ax = ax.reshape(-1)
    if labels == []:
        for i,d in enumerate(args):
            labels.append(f"data {i+1}")

    for i,c in enumerate(channels):
        for j, data in enumerate(args):
            ax[i].plot(data[:,c].reshape(-1), label=labels[j])
        ax[i].legend()
        ax[i].set_title(f"Channel {c}")

    plt.show()
