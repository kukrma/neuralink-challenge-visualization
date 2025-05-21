# =========================================================================== #
# --- SEMINAR WORK (preprocessing.py) --------------------------------------- #
#     title:   Neuralink Compression Challenge: Web-based Interactive         #
#              Visualization of N1 Implant Signals and Inter-Channel          #
#              Correlations in Python                                         #
#     author:  Martin KUKRÁL                                                  #
#     subject: KIV/VI                                                         #
#     year:    2024/2025                                                      #
# =========================================================================== #
# ----------------- #
# Python   3.11.4   #
# ----------------- #
# numpy    1.25.2   #
# os       built-in #
# pandas   2.1.0    #
# scipy    1.11.2   #
# tqdm     4.66.1   #
# ----------------- #
import os
import numpy as np
from tqdm import tqdm
import pandas as pd
from scipy.io import wavfile
from scipy.cluster.hierarchy import linkage, leaves_list





# === LOAD THE DATA ===========================================================
signals = []        # will be filled with signals
maxlen = 99903      # longest channel (known from previous runs)
minlen = 98567      # shortest channel (known from previous runs)
sample_rate = 19531 # same for all channels (known from previous runs)
# load all channels and concatenate them into one np.array:
for file in tqdm(os.listdir("data/raw")):
    # file content:
    _, signal = wavfile.read(f"data/raw/{file}")
    # testing the signal length (padding if necessary):
    if len(signal) < maxlen:
        # add paddingu:
        padsize = maxlen - len(signal)             # paddingu size
        padding = np.zeros(padsize)                # pad with zeroes
        signal = np.concatenate((signal, padding)) # signal + padding
    # save the signal into the array:
    signals.append(signal)
# turn the list of signals into a np.array:
signals = np.array(signals)
# print relevant values:
channels = signals.shape[0]
print(f"POČET ELEKTROD:       {channels}")
print(f"MAX POČET VZORKŮ:     {maxlen}")
print(f"MIN POČET VZORKŮ:     {minlen}")
print(f"VZORKOVACÍ FREKVENCE: {sample_rate} Hz")
# save the signal:
np.save("data/signals.npy", signals)



# === CORRELATION ANALYSIS ====================================================
'''
# TAKES A FEW HOURS TO COMPLETE
signals_df = pd.DataFrame(signals.T[:minlen]) # convert to dataframe to make it faster
corrP = signals_df.corr(method="pearson")     # correlation matrix (Pearson)
corrS = signals_df.corr(method="spearman")    # correlation matrix (Spearman)
corrK = signals_df.corr(method="kendall")     # correlation matrix (Kendall)
# save the correlation matrices:
np.save("data/corrP.npy", corrP.values) # save correlation matrix (Pearson)
np.save("data/corrS.npy", corrS.values) # save correlation matrix (Spearman)
np.save("data/corrK.npy", corrK.values) # save correlation matrix (Kendall)
'''


# === REORDERING ==============================================================
corrP = np.load("data/corrP.npy") # correlation matrix (Pearson)
corrS = np.load("data/corrS.npy") # correlation matrix (Spearman)
corrK = np.load("data/corrK.npy") # correlation matrix (Kendall)
# compute the hierarchical clustering using selected methods:
for method in tqdm(["single", "average", "centroid", "ward"]):
    # compute the hierarchical models for correlation matrices:
    linkageP = linkage(corrP, method=method) # correlation matrix hierarchy (Pearson)
    linkageS = linkage(corrS, method=method) # correlation matrix hierarchy (Spearman)
    linkageK = linkage(corrK, method=method) # correlation matrix hierarchy (Kendall)
    # retrieve the reordered channels:
    orderP = np.array(leaves_list(linkageP)) # reordered channels (Pearson)
    orderS = np.array(leaves_list(linkageS)) # reordered channels (Spearman)
    orderK = np.array(leaves_list(linkageK)) # reordered channels (Kendall)
    # save the reordered channels for the selected method:
    np.save(f"data/order_P_{method}.npy", orderP) # saved reordering (Pearson)
    np.save(f"data/order_S_{method}.npy", orderS) # saved reordering (Spearman)
    np.save(f"data/order_K_{method}.npy", orderK) # saved reordering (Kendall)