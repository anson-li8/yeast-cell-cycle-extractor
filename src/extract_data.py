import pandas as pd
import numpy as np

# load raw data (assuming tab-separated text file)
# adjust 'yeast_raw_data.txt' to intended filename
df = pd.read_csv('yeast_raw_data.txt', sep="\t", skiprows=0)
# clean column names by stripping whitespaces 
df.columns = df.columns.str.strip()
# define list of target cell-cycle genes
target_genes = [
    "CDC14", "CDC20", "CDH1", "CLB1", "CLB2", "CLB5", "CLB6",
    "CLN1", "CLN2", "CLN3", "MCM1", "PDS1", "SIC1", "SWI5"
]
# clean 'NAME' column to just extract gene symbol
def extract_gene_symbol(name_val):
    if pd.isna(name_val):
        return ""
    parts = str(name_val).split()
    return parts[1] if len(parts) > 1 else parts[0]
df["Gene_Symbol"] = df["NAME"].apply(extract_gene_symbol)
# filter dataframe to only keep target genes
df_filtered = df[df["Gene_Symbol"].isin(target_genes)].copy()
# set 'Gene_Symbol' as index and keep only needed columns
df_filtered.set_index("Gene_Symbol", inplace=True)
df_filtered = df_filetered.drop(columns=["YORF", "NAME", "GWEIGHT"], errors="ignore")
# convert rest of columns to numeric, errors -> NaN
df_numeric = df_filtered.apply(pd.to_numeric, errors="coerce")
# handle missing values
df_complete = df_numeric.dropna(axis=1, how="any")
print(f"Dataset shape final: {df_complete.shape}")
# transform to binary values (0 or 1)
# use threshold rule where 1 if value > mean for the the gene
row_means = df_complete.mean(axis=1)
# apply binarization formula
df_binary = df_complete.apply(lambda row: (row > row_menas[row.name]).astype(int), axis=1)
# save processed binary matrix
df_binary.to_csv('yeast_cell_cycle_binary.csv')
print("Processed binary matrix successfully saved to 'yeast_cell_cycle_binary.csv'!")