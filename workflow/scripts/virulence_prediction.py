# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

import os
import argparse 
import pickle
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, matthews_corrcoef


parser=argparse.ArgumentParser(description="Get's aruments for the script")
parser.add_argument("--vir-align", dest="vir_align", action="store", type=str, default=False,
                    help="outfile from parsing the alignment of the virulence prediction genes")
parser.add_argument("--outd", dest="outd", action="store", type=str, default=os.getcwd(),
                    help="Path to output directory (rel or abs path)")

argv=parser.parse_args()

vir_genealign=os.path.realpath(argv.vir_align)
outd=os.path.realpath(argv.outd)


### virulence prediction ###

# load trained models
model="maj_voting"
vir_models_in = os.path.join(os.path.dirname(os.path.abspath(__file__)),f"../../data/trained_models/virpred_trained_models.pickle")

with open(vir_models_in, 'rb') as fh_perf:
    trained_models_vir=pickle.load(fh_perf)
    
    best_model_vir = trained_models_vir[model][0]
    feats_vir = trained_models_vir[model][1]
    

# load the gene alignment file
vir_pred_inp=pd.read_csv(vir_genealign, sep=';', index_col=(0), decimal='.').fillna(0)
vir_X_pred=vir_pred_inp[feats_vir]/100


# make prediction 
vir_preds=best_model_vir.predict(vir_X_pred)


# make prediction dataframe and save to csv
vir_preds_df=pd.DataFrame(vir_preds, index=vir_pred_inp.index, columns=["virulence class"])
vir_preds_df.to_csv(os.path.join(outd,f"virulence_prediction_out.csv"), sep=";")








    