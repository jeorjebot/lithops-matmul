# Matrix multiplication with Lithops

## Requirements
```console
python3 -m pip install -r requirements.txt
```
## Usage 
```console
python matrix_multiplication.py mode A_rows A_cols B_rows B_cols block_size
```

## Example 
### Plain approach
```console
python matrix_multiplication.py plain 10 20 20 10 2
```
### Encrypted approach
```console
python matrix_multiplication.py encrypted 10 20 20 10 2
```

## Parameters
- mode: **plain** or **encrypted**.
- A_rows, A_cols: the sizes of the first matrix.
- B_rows, B_cols: the sizes of the second matrix.
- block_size: for grouping the rows of the first matrix and the columns of the second matrix on row-blocks and column-blocks respectively.

## Repository structure
```
├── examples
│   ├── lithops_hello_world.py
│   └── paillier.py
├── data
│   ├── time_dims.txt
│   ├── time_local_cloud.txt
│   ├── time_plain_encr.txt
│   └── time_plain_encr_old.txt
├── notebooks
│   └── plot_results.ipynb
├── tests
│   ├── test_time_local_cloud.sh
│   ├── test_time_plain.sh
│   └── test_time_plain_vs_encr.sh
├── reports
│   ├── SDSA___Assignment_3.pdf
│   └── images
│       ├── block-size.png
│       ├── colsA-rowsB.png
│       ├── plain-local-cloud.png
│       ├── plain-vs-encr-cloud-not-scaled.png
│       ├── plain-vs-encr-cloud-scaled.png
│       ├── plain-vs-encr.png
│       ├── rowsA-colsB.png
│       └── rowscolsA-rowscolsB.png
│ 
├── matrix_multiplication.py
├── README.md
└──requirements.txt
```

## Author
**Author: Giorgio Rossi**
