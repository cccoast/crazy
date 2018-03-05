# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os

dfs = {}
base_dir = r'E:\2015\exam\classify'

def classify():
    for root,sub,fnames in os.walk(base_dir):
        for i,ifile in enumerate(fnames):
            icsv = os.path.join(root,ifile)
            dfs[i] = pd.read_csv(icsv,index_col = 0,encoding = 'cp936')
            

if __name__ == '__main__':
    classify()