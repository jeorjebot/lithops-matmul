# Authors: Marc Sanchez Artigas <marc.sanchez@urv.cat>
# License: BSD 3 clause
import numpy as np
import sys
import pickle
from lithops import FunctionExecutor, Storage

def matrix_print(mat, tab='', fmt='g'):
    '''
        Pretty print a matrix
    '''
    output = ''
    col_maxes = [max([len(('{:'+fmt+'}').format(x))
                      for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            output += ('{}{:'+str(col_maxes[i])+fmt +
                       '}  ').format(((i == 0) and tab or ''), y)
        output += '\n'
    return output


def mul_row_col_plain(A, B, block_size):
    '''
        Matrix multiplication by row-blocks of size A_rows x block_size
        and column-blocks of size block_size x B_cols
    '''

    # Get number of rows in matrix A
    A_rows = A.shape[0]
    # Get number of columns in matrix B
    B_cols = B.shape[1]

    # C is of size A_rows x B_cols
    C = np.zeros((A_rows, B_cols))

    namespace = 'plain-matmul'
    fexec = FunctionExecutor(mode='localhost')
    storage = Storage() 

    position = 0
    for i in range(int(A_rows/block_size)):
        for j in range(int(B_cols/block_size)):
            row_block = A[i*block_size:(i+1)*block_size, :]
            col_block = B[:, j*block_size:(j+1)*block_size]
            args = {'namespace': namespace, 'row_block': row_block, 'col_block': col_block, 'position': position}

            fexec.call_async(dot_product_plain, args)

            # serialize the matrix
            position += 1

            # C = dot product rows x cols
            #C[i*block_size:(i+1)*block_size, j*block_size:(j+1)* block_size] = fexec.get_result()
    
    fexec.wait()
    fexec.call_async(result, namespace)
    C = fexec.get_result()
    return C
    

def result(namespace, storage):
    C = storage.get_object(namespace, str(0))
    return pickle.loads(C)

def dot_product_plain(namespace, row_block, col_block, position, storage):
    result = np.dot(row_block, col_block)
    storage.put_object(namespace, str(position), pickle.dumps(result))


def check_parameters(A_rows, A_cols, B_rows, B_cols, block_size):
    if not A_cols == B_rows:
        raise ValueError(f'''The number of columns in matrix A
                    must be equal to the number of rows in matrix B.''')

    if A_rows % block_size != 0:
        raise ValueError(
            f'The number of rows in A is not divisible by {block_size}')

    if B_cols % block_size != 0:
        raise ValueError(
            f'The number of columns in B is not divisible by {block_size}')

if __name__ == '__main__':
    if len(sys.argv) == 7:
        #TODO: check the cast
        mode = sys.argv[1]
        A_rows = int(sys.argv[2])
        A_cols = int(sys.argv[3])
        B_rows = int(sys.argv[4])
        B_cols = int(sys.argv[5])
        block_size = int(sys.argv[6])

        check_parameters(A_rows, A_cols, B_rows, B_cols, block_size)

        A = np.random.randint(10, size=(A_rows, A_cols))
        B = np.random.randint(10, size=(B_rows, B_cols))

        C = mul_row_col_plain(A, B, block_size)
        print(C)
        #print(f'\n[*] Matrix product using mul_row_col_plain(·) is:\n{matrix_print(C)}')

    else:
        print(
            "[*] Usage: python mult_row_column.py mode A_rows A_cols B_rows B_cols block_size ")

"""
    C = np.matmul(A, I)
    print(f'Matrix product using matmul(·) is:\n{matrix_print(C)}')
"""