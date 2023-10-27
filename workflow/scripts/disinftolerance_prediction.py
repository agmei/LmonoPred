# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)


import os
import argparse
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, matthews_corrcoef


parser=argparse.ArgumentParser(description="Get's aruments for the script")
parser.add_argument("--disinf-align", dest="disinf_align", action="store", type=str, default=False,
                    help="outfile from parsing the gene alignment of the disinfectant prediction genes")
parser.add_argument("--outd", dest="outd", action="store", type=str, default=os.getcwd(),
                    help="Path to output directory (rel or abs path)")

argv=parser.parse_args()

disinf_genealign=os.path.realpath(argv.disinf_align)
outd=os.path.realpath(argv.outd)


### disinfectant class prediction ###

# load trained models
disinf_models_in = os.path.join(os.path.dirname(os.path.abspath(__file__)),f"../../data/trained_models/disinfpred_trained_model.joblib")

best_model_disinf = joblib.load(disinf_models_in)


# load the gene alignment file
disinf_pred_inp=pd.read_csv(disinf_genealign, sep=';', index_col=(0), decimal='.').fillna(0)
disinf_X_pred=disinf_pred_inp/100

# make prediction 
disinf_preds=best_model_disinf.predict(disinf_X_pred)


# make prediction dataframe and save to csv
disinf_preds_df=pd.DataFrame(disinf_preds, index=disinf_pred_inp.index, columns=["disinfectant phenotype"])
disinf_preds_df.to_csv(os.path.join(outd,f"disinftolerance_prediction_out.csv"), sep=";")







    