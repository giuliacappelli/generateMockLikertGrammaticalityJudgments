import argparse
from doepy import build, read_write
import pandas as pd
import random
import numpy as np

# Given Input factors, adjUst LIkert Acceptability judgments based on levels

my_parser = argparse.ArgumentParser()

my_parser.add_argument('--factors',
                       '-f',
                       action='store',
                       default='input_factors.csv',
                       help='file containing tab-separated factors and levels')
                       
my_parser.add_argument('--output',
                       '-o',
                       action='store',
                       default='mock_judgments.csv',
                       help='output file with mock judgments')
                       
my_parser.add_argument('--participants',
                       '-p',
                       type=int,
                       action='store',
                       default='25',
                       help='number of participants to the experiment')                       

args = my_parser.parse_args()

# create dictionary from input file to create Cartesian product dataframe using doepy
dict_input = {}
with open(args.factors, "r") as file_input:
	for line in file_input:
		listline = line.strip().split("\t")
		if len(listline)>0:
			factor = listline[0]
			levels = listline[1:]
			dict_input[factor] = levels
			
df_raw = build.full_fact(dict_input) # doepy function to compute Cartesian product of levels

# set number of participants to the experiment
n_prtps = args.participants

# create a column for each participant with random judgments on a given Likert scale
for el in range(n_prtps):
	df_raw["prtp"+str(el+1)] = np.random.randint(7, 8, df_raw.shape[0]) # range 1-7
	# ~ df_raw["prtp"+str(el+1)] = np.random.randint(6, 8, df_raw.shape[0]) # only 6s and 7s to initialize constrained judgments

# subset of df_raw containing only judgment columns
df_part = df_raw.filter(regex='prtp').copy()   # .copy() quenches SettingwithCopyWarning's thirst for blood
df_factors = df_raw[dict_input.keys()].astype(int)

# here comes the fun! update your random judgments based on some constraints (here I implemented the one I need)
for num in list(df_part.index.values): # for each index in the list of df_part row indexes
	for factor in list(df_factors.columns): # for each factor in design
		df_part.loc[num] -= [df_factors[factor].loc[num]] # subtract factor score/weight (= level name in doepy) from judgments

# replaces a given percentage of df_part values with random values (bounded by df_part values) to add noise in the judgments
for el in range(n_prtps):
	df_part["prtp"+str(el+1)] = df_part["prtp"+str(el+1)].sample(frac=0.7) # replace 30% of values in each column with NaNs
	df_part = df_part.apply(lambda x: np.where(x.isnull(), x.dropna().sample(len(x), replace=True), x)) # replace NaNs with values in column
	df_part = df_part.apply(lambda x: np.where(x<=0, x.dropna().sample(len(x), replace=True), x)) # replace 0s with values in column

# merge back the judgments and the factor columns
df_new = df_part.join(df_raw[df_raw.columns.difference(df_part.columns)]) 

read_write.write_csv(df_new.astype(int),filename=args.output)
