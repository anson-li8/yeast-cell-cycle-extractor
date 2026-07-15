import argparse
import pandas as pd
import numpy as np
from pathlib import Path


def extract_gene_symbol(name_val):
    if pd.isna(name_val):
        return ""
    parts = str(name_val).split()
    return parts[1] if len(parts) > 1 else parts[0]


def process_expression_data(
    input_file_path: Path,
    output_file_path: Path,
    target_genes: list,
    id_col: str = "NAME",
    cols_to_drop: list = None
):
    if cols_to_drop is None:
        cols_to_drop = ["YORF", "NAME", "GWEIGHT"]
    print(f" Reading raw data from: {input_file_path}")
    df = pd.read_csv(input_file_path, sep="\t", skiprows=0)
    # clean column names by stripping whitespaces
    df.columns = df.columns.str.strip()
    # extract gene symbols then filter dataframe to only keep target genes
    df["Gene_Symbol"] = df["NAME"].apply(extract_gene_symbol)
    df_filtered = df[df["Gene_Symbol"].isin(target_genes)].copy()
    # set 'Gene_Symbol' as index and keep only needed columns
    df_filtered.set_index("Gene_Symbol", inplace=True)
    df_filtered = df_filtered.drop(columns=cols_to_drop, errors="ignore")
    # convert rest of columns to numeric, errors -> NaN
    df_numeric = df_filtered.apply(pd.to_numeric, errors="coerce")
    # handle missing values
    df_complete = df_numeric.dropna(axis=1, how="any")
    print(f"Dataset shape final: {df_complete.shape}")
    if df_complete.empty:
        raise ValueError(
            "Error: Filtering resulted in an empty dataset. Check your gene names or missing values.")
    # transform to binary values (0 or 1)
    # use threshold rule where 1 if value > mean for the the gene
    row_means = df_complete.mean(axis=1)
    # apply binarization formula
    df_binary = df_complete.apply(lambda row: (
        row > row_means[row.name]).astype(int), axis=1)
    # maek sure parent output directory exists before saving
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    # Save output
    df_binary.to_csv(output_file_path)
    print(f" Success! Binarized data saved to: {output_file_path}\n")


if __name__ == "__main__":
    # find project directory paths
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    DEFAULT_INPUT = PROJECT_ROOT / "data" / "raw" / "yeast_raw_data.txt"
    DEFAULT_OUTPUT = PROJECT_ROOT / "data" / \
        "processed" / "yeast_cell_cycle_binary.csv"
    DEFAULT_GENES = [
        "CDC14", "CDC20", "CDH1", "CLB1", "CLB2", "CLB5", "CLB6",
        "CLN1", "CLN2", "CLN3", "MCM1", "PDS1", "SIC1", "SWI5"
    ]
    # allow command line overrides for reproductibility
    parser = argparse.ArgumentParser(
        description="Clean and binarize genomic microarray datasets.")
    parser.add_name = "Yeast Extractor"
    parser.add_argument("--input", type=str, default=str(DEFAULT_INPUT),
                        help="Path to input raw data file")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT),
                        help="Path to save processed binary CSV")
    parser.add_argument("--genes", type=str, nargs="+",
                        default=DEFAULT_GENES, help="List of target genes to filter")
    args = parser.parse_args()
    # Run process
    process_expression_data(
        input_file_path=Path(args.input),
        output_file_path=Path(args.output),
        target_genes=args.genes
    )
