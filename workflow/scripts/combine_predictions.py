import os
import argparse
import pandas as pd



parser=argparse.ArgumentParser(description="Get's aruments for the script")
parser.add_argument("--vir-pred", dest="vir_pred", action="store", type=str, default=False,
                    help="outfile from virulence prediction")
parser.add_argument("--disinf-pred", dest="disinf_pred", action="store", type=str, default=False,
                    help="outfile from disinfectant tolerance prediction")
parser.add_argument("--outd", dest="outd", action="store", type=str, default=os.getcwd(),
                    help="Path to output directory (rel or abs path)")

argv=parser.parse_args()

vir_pred=os.path.realpath(argv.vir_pred)
disinf_pred=os.path.realpath(argv.disinf_pred)
outd=os.path.realpath(argv.outd)


# load the gene virulence prediction file
vir_preds_df=pd.read_csv(vir_pred, sep=';', index_col=(0), decimal='.')

# load the disinfectant tolerance prediction file
disinf_preds_df=pd.read_csv(disinf_pred, sep=';', index_col=(0), decimal='.')


# rename dicts 
dis_num={1: 0,
         2: 1}
vir_cat={1: "low",
         2: "medium",
         3: "high"}
dis_cat={1: "susceptible",
         2: "tolerant"}

# make prediction dataframe and save to csv (numerical output)
comb_preds_df_num=vir_preds_df.join(disinf_preds_df.replace(dis_num))
comb_preds_df_num.to_csv(os.path.join(outd, "combined_predictions_out_numerical.csv"), sep=";")


# make prediction dataframe and save to csv (categorical output)
comb_preds_df_cat=vir_preds_df.replace(vir_cat).join(disinf_preds_df.replace(dis_cat))
comb_preds_df_cat.to_csv(os.path.join(outd, "combined_predictions_out_categorical.csv"), sep=";")






    