import numpy as np
import sys
import pickle
import phe as paillier
from lithops import FunctionExecutor, Storage

def matrix_multiplication(A_rows, B_cols, block_size):
    '''
        Matrix multiplication computed on row-blocks (matrix A) and column-blocks
        (matrix B), obtained from the storage. Each each resulting submatrix is
        also stored on the storage.
    '''
    for row in range(int(A_rows/block_size)):
        for col in range(int(B_cols/block_size)):
            row_block = pickle.loads(storage.get_object(namespace, f'row_{row}'))
            col_block = pickle.loads(storage.get_object(namespace, f'column_{col}'))
            args = {'namespace': namespace, 'row_block': row_block, 'col_block': col_block, 'row_index': row, 'col_index': col}
            fexec.call_async(dot_product_plain, args)
    fexec.wait()


def dot_product_plain(namespace, row_block, col_block, row_index, col_index, storage):
    result_block = np.dot(row_block, col_block)
    storage.put_object(namespace, f'row_{row_index}_column_{col_index}', pickle.dumps(result_block))


def store_matrix_plain(dim1, dim2, block_size, axis='row'):
    '''
        The plain matrix is created row-block by row-block, or column-block by column-block,
        depending on the axis parameter, and then stored in the storage.
    '''
    if(axis == 'column'):
        for index in range(int(dim2/block_size)):
            block = np.random.randint(10, size=(dim1, block_size))#.tolist()
            args = {'namespace': namespace, 'block': block, 'index': index, 'axis': axis}
            fexec.call_async(store, args)
    else:
        for index in range(int(dim1/block_size)):
            block = np.random.randint(10, size=(block_size, dim2))#.tolist()
            args = {'namespace': namespace, 'block': block, 'index': index, 'axis': axis}
            fexec.call_async(store, args)
    fexec.wait()


def store_matrix_encrypted(dim1, dim2, block_size, axis='row'):
    '''
        The encrypted matrix is created row-block by row-block, or column-block by column-block,
        depending on the axis parameter, and then stored in the storage.
    '''
    if(axis == 'column'):
        for index in range(int(dim2/block_size)):
            plain_block = np.random.randint(10, size=(dim1, block_size)).tolist()
            encrypted_block = [[pubkey.encrypt(col) for col in plain_block[row]] for row in range(len(plain_block))]
            block = np.array(encrypted_block)
            args = {'namespace': namespace, 'block': block, 'index': index, 'axis': axis}
            fexec.call_async(store, args)
    else:
        for index in range(int(dim1/block_size)):
            plain_block = np.random.randint(10, size=(block_size, dim2)).tolist()
            encrypted_block = [[pubkey.encrypt(col) for col in plain_block[row]] for row in range(len(plain_block))]
            block = np.array(encrypted_block)
            args = {'namespace': namespace, 'block': block, 'index': index, 'axis': axis}
            fexec.call_async(store, args)
    fexec.wait()


def store(namespace, block, index, axis, storage):
    storage.put_object(namespace, f'{axis}_{index}', pickle.dumps(block))


# not used in the implementation
def store_encrypted(namespace, block, index, axis, storage):
    # encryption with paillier
    encr_block_list = [[pubkey.encrypt(col) for col in block[row]] for row in range(len(block))]
    block = np.array(encr_block_list)
    storage.put_object(namespace, f'{axis}_{index}', pickle.dumps(block))


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


def test():
    row = pickle.loads(storage.get_object(namespace, 'row_0'))
    column = pickle.loads(storage.get_object(namespace, 'column_0'))
    submatrix = pickle.loads(storage.get_object(namespace, 'row_0_column_0'))
    
    # assert that the result submatrix in position (0, 0) is a square matrix
    assert submatrix.shape[0] == submatrix.shape[0]
    print('\nMatrix A, row-block 0 : ')
    print(row)
    print('\nMatrix B, column-block 0 : ')
    print(column)
    print('\nMatrix Result, block (0,0) : ')
    print(submatrix)



if __name__ == '__main__':
    # numpy seed
    np.random.seed(0)

    if len(sys.argv) == 7:
        try:
            mode = sys.argv[1]
            A_rows = int(sys.argv[2])
            A_cols = int(sys.argv[3])
            B_rows = int(sys.argv[4])
            B_cols = int(sys.argv[5])
            block_size = int(sys.argv[6])
        except: 
            raise ValueError(f'Error with input parameters')

        check_parameters(A_rows, A_cols, B_rows, B_cols, block_size)

        fexec = FunctionExecutor(mode='localhost')
        storage = Storage()
        namespace = mode

        if(mode == 'plain'):
            # create and store PLAIN matrix A on object storage
            store_matrix_plain(A_rows, A_cols, block_size, axis='row')

            # create and store PLAIN matrix B on object storage
            store_matrix_plain(B_rows, B_cols, block_size, axis='column')

            # matrix multiplication
            matrix_multiplication(A_rows, B_cols, block_size)

            # just to be sure
            test()

        if(mode == 'encrypted'):
            pubkey, privkey = paillier.generate_paillier_keypair()
            
            # create and store PLAIN matrix A on object storage
            store_matrix_plain(A_rows, A_cols, block_size, axis='row')

            # create and store ENCRYPTED matrix B on object storage
            store_matrix_encrypted(B_rows, B_cols, block_size, axis='column')

            # matrix multiplication
            matrix_multiplication(A_rows, B_cols, block_size)

            # just to be sure
            test()

        else:
            print("[*] Mode not available")
            print("[*] Usage: python matrix_multiplication.py mode A_rows A_cols B_rows B_cols block_size")

    else:
        print("[*] Usage: python matrix_multiplication.py mode A_rows A_cols B_rows B_cols block_size")

