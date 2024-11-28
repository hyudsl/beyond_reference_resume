import os
import sys
import pandas as pd
import argparse
from argparse import ArgumentParser

def make_positive_relative_score(df:pd.DataFrame, args:argparse.Namespace) -> pd.DataFrame:
    ref_col = args.ref_col_name
    cand_col = args.cand_col_name
    rating_col = args.rating_col_name
    
    _df = df.copy()
    
    # Calculate relative score
    _df[rating_col] = 100 - df[rating_col]
    
    # Normalize the human score rating: [0,100] -> [0,1]
    _df[rating_col] = _df[rating_col] / 100
    
    # reference slot: candidate / candidate slot: reference
    _df[ref_col] = df[cand_col]
    _df[cand_col] = df[ref_col]
    
    return _df


def make_negative_relative_score(df:pd.DataFrame, args:argparse.Namespace) -> pd.DataFrame:
    rating_col = args.rating_col_name
    
    _df = df.copy()
    
    # Calculate relative score
    _df[rating_col] = df[rating_col] - 100
    
    # Normalize the human score rating: [0,100] -> [0,1]
    _df[rating_col] = _df[rating_col] / 100
    
    return _df
    


if __name__ =='__main__':
    parser = ArgumentParser()
    parser.add_argument('--csv_data_path', type=str)
    parser.add_argument('--src_col_name', type=str, default='src')
    parser.add_argument('--ref_col_name', type=str, default='ref')
    parser.add_argument('--cand_col_name', type=str, default='cand')
    parser.add_argument('--rating_col_name', type=str, default='score')
    parser.add_argument('--output_path', type=str)
    
    args = parser.parse_args()
    
    ## Load data
    if not os.path.exists(args.csv_data_path):
        print(f"The path of data \"{args.csv_data_path}\" does not exist.")
        sys.exit(0)
        
    if not args.csv_data_path.endswith("csv"):
        print("The input data must be csv file.")
        sys.exit(0)
    
    df = pd.read_csv(args.csv_data_path)
    
    negative_relative_score_df = make_negative_relative_score(df, args)
    positive_relative_score_df = make_positive_relative_score(df, args)
    
    ## Create output directory
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)
        
    negative_relative_score_df.to_csv(os.path.join(args.output_path,"negative_relative_score.csv"),
                                      index=False)
    
    positive_relative_score_df.to_csv(os.path.join(args.output_path, "positive_relaitve_score.csv",
                                                   index=False))
    
    print(f"Saved data: {args.output_path}")
