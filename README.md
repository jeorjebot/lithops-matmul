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

## Author
**Author: Giorgio Rossi**
