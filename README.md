# Neuralink Compression Challenge: Web-based Interactive Visualization of N1 Implant Signals and Inter-Channel Correlations in Python

This GitHub repository hosts the seminar project for the **KIV/VI (*Information Visualization*)** course, which is part of the curriculum at the **Department of Computer Science and Engineering, Faculty of Applied Sciences, University of West Bohemia**.

[![CC BY-NC 4.0][cc-by-nc-shield]][cc-by-nc]

[![CC BY-NC 4.0][cc-by-nc-image]][cc-by-nc]

[cc-by-nc]: https://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]: https://licensebuttons.net/l/by-nc/4.0/88x31.png
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg

## How to Use
To use this code, you first need to install Python on your computer and optionally some IDE in which you can comfortably interact with the scripts. Specifically, I have used **Python version 3.11.4** and the following libraries:
| LIBRARY      | VERSION     |
| ------------ | ----------- |
| dash         | 3.0.3       |
| numpy        | 1.25.2      |
| os           | built-in    |
| pandas       | 2.1.0       |
| plotly       | 5.22.0      |
| scipy        | 1.11.2      |
| tqdm         | 4.66.1      |

With everything prepared, the code should be ready to use. One you launch the `app.py` script, the application can be accessed locally on URL: [http://127.0.0.1:8050/](http://127.0.0.1:8050/) via any web browser as long as the script is running.

The application does not work without the necessary data, which is not published on this repository due to its significant size. Luckily, the entire dataset is publicly available on the *Neuralink Compression Challenge* website:

[<img src="https://img.shields.io/badge/URL-Neuralink Compression Challenge-white">](https://content.neuralink.com/compression-challenge/README.html)

With the downloaded dataset, it is possible to preprocess it using the provided script `preprocess.py`.

## Description of Files
The seminar work is structured as follows:
```
├── bin/                                                      - contains the application and data
│   ├── assets/                                                 - contains additional files for the website
│   │   ├── favicon.ico                                           - website icon
│   │   └── style.css                                             - CSS styling for the website
│   ├── data/                                                   - contains data
│   │   ├── raw/                                                  - contains raw data from the Neuralink website
│   │   │   ├── **00d4f842-fc92-45f5-8cae-3effdc2245f5.wav**        - CH1 raw N1 signal
│   │   │   ├── **00dc461c-a60a-4d74-bf87-de4208f224ee.wav**        - CH2 raw N1 signal
│   │   │   └── ...                                                 - ...
│   │   ├── corrK.npy                                             - correlation matrix (Kendall's tau)
│   │   ├── corrP.npy                                             - correlation matrix (Pearson's correlation coefficient)
│   │   ├── corrS.npy                                             - correlation matrix (Spearman's rank correlation coefficient)
│   │   ├── order_K_average.npy                                   - reordering indices (Kendall, UPGMA)
│   │   ├── order_K_centroid.npy                                  - reordering indices (Kendall, UPGMC)
│   │   ├── order_K_single.npy                                    - reordering indices (Kendall, Nearest Point)
│   │   ├── order_K_ward.npy                                      - reordering indices (Kendall, Ward)
│   │   ├── order_P_average.npy                                   - reordering indices (Pearson, UPGMA)
│   │   ├── order_P_centroid.npy                                  - reordering indices (Pearson, UPGMC)
│   │   ├── order_P_single.npy                                    - reordering indices (Pearson, Nearest Point)
│   │   ├── order_P_ward.npy                                      - reordering indices (Pearson, Ward)
│   │   ├── order_S_average.npy                                   - reordering indices (Spearman, UPGMA)
│   │   ├── order_S_centroid.npy                                  - reordering indices (Spearman, UPGMC)
│   │   ├── order_S_single.npy                                    - reordering indices (Spearman, Nearest Point)
│   │   ├── order_S_ward.npy                                      - reordering indices (Spearman, Ward)
│   │   └── **signals.npy**                                       - preprocessed N1 signals
│   ├── app.py                                                  - script to launch the application
│   └── preprocessing.py                                        - script to do raw N1 signal preprocessing
└── doc/                                                      - contains the documentation/short paper
    ├── kukral_VI_documentation.pdf                             - PDF with the documentation/short paper
    └── kukral_VI_latex.zip                                     - LaTeX source files for the documentation
```

Files enclosed by `**...**` are not part of this GitHub repository due to their size. The signals in the `raw/` folder (which is empty in this repository) can be downloaded from the above mentioned *Neuralink Compression Challenge* website and the `signals.npy` file is created during the execution of the `preprocess.py` script. Thanks to the provided pre-computed correlation matrices and reordering indices, it is possible to save a lot of time when executing the `preprocess.py` script, as they take a long time (especially the correlation analysis).
