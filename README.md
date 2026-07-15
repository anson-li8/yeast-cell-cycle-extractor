# Yeast Cell-Cycle Gene Expression Extractor

Simple Python script to filter, clean, and convert continuous yeast microarray data into binary (0/1) values. This is designed to prepare raw data from the classic Gasch yeast studies for Boolean cell-cycle network modeling. (Build specifically for the BBNI package real-world implementation section [here](https://anson-li8.github.io/BBNI/articles/Introduction_to_BBNI.html))

It targets 14 specific cell-cycle genes: `CDC14`, `CDC20`, `CDH1`, `CLB1`, `CLB2`, `CLB5`, `CLB6`, `CLN1`, `CLN2`, `CLN3`, `MCM1`, `PDS1`, `SIC1`, and `SWI5`.

## How it Works
1.  **Filtering:** Pulls out 14 target cell-cycle genes from a raw genomic dataset of over 6,000 genes.
2.  **Cleaning:** Drops any experiment columns that contain missing values (`NaN`s) so you only work with complete data.
3.  **Binarizing:** Calculates the mean ($\mu$) for each individual gene. If a value is higher than that gene's average, it becomes a `1` (active). If it's equal to or lower than the average, it becomes a `0` (inactive).

$$\text{State}(x) = \begin{cases} 1 & \text{if } x > \mu \\ 0 & \text{if } x \le \mu \end{cases}$$

## Project Structure

```

yeast-cell-cycle-extractor/
├── data/
│   ├── raw/                  # put raw yeast_raw_data.txt file here
│   └── processed/            # script will save clean binary CSV here
├── src/
│   └── extract_data.py       # main Python cleaning script
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Getting Started

### Prerequisites

Make sure you have Python 3.8 or higher installed on your computer.

### Setup

Clone this repository and install prerequisites:

```

git clone https://github.com/anson_li8/yeast-cell-cycle-extractor.git
cd yeast-cell-cycle-extractor
pip install -r requirements.txt
```

### Usage

1.  Put your raw data file inside the `data/raw/` folder.
2.  Run the script from the root folder:
```

# Run with default settings (looks for data/raw/yeast_raw_data.txt)
python src/extract_data.py
```
If you want to run it on a different raw file or target a different list of genes, you can use the built-in command-line flags:
```

python src/extract_data.py --input data/raw/other_data.txt --output data/processed/clean_output.csv --genes ACT1 MYO1
```

## Data Source

The raw data is from the **Gasch Lab at UW-Madison**:
*   **Paper:** _Genomic Expression Responses to DNA-damaging Agents and the Regulatory Role of the Yeast ATR Homolog Mec1p_ (Gasch et al., 2001).
*   **Where to find it:** [Supplemental Dataset](https://pmc.ncbi.nlm.nih.gov/articles/PMC60150/).