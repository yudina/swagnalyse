# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 17:29:27 2018

@authors: kevin, yujia
"""
import sys
import time
from math import ceil, log

ex_path1 = sys.argv[1] # Path of the first matrix
ex_path2 = sys.argv[2] # Path of the second matrix

global LEAF_SIZE
LEAF_SIZE = 1 # For a no-threshold strassen

def extractMatrix(file_name):
    new_matrix = []
    
    with open(file_name,'r') as file:
        for line in file:
            line = line.strip()
            if len(line) > 1:
               new_matrix.append([int(a) for a in line.split()])
    file.close()
    
    return new_matrix

# Make an algebric addition of 2 same dimensions matrices
def add(matrix_A, matrix_B):
    
    # matrix initialization
    length = len(matrix_A)
    matrix_C = [[0 for j in range(0, length)] for i in range(0, length)]
    
    # addition on each element
    for i in range(0, length):
        for j in range(0, length):
            matrix_C[i][j] = matrix_A[i][j] + matrix_B[i][j]
    return matrix_C

# Make an algebric substraction of 2 same dimensions matrices
def subtract(matrix_A, matrix_B):
    
    # matrix initialization
    length = len(matrix_A)
    matrix_C = [[0 for j in range(0, length)] for i in range(0, length)]
    
    # substraction on each element
    for i in range(0, length):
        for j in range(0, length):
            matrix_C[i][j] = matrix_A[i][j] - matrix_B[i][j]
    return matrix_C

# The simple algorithm used under the leaf_size value (recursion threshold)
def conventionnalProduct(matrix_A, matrix_B):    
    
    # matrix initialization
    w, h = len(matrix_A[0]), len(matrix_B[0]);
    matrix_C = [[0 for x in range(w)] for y in range(h)]
    
    for i in range(len(matrix_A)):
       # iterate through columns of Y
       for j in range(len(matrix_B[0])):
           # iterate through rows of Y
           for k in range(len(matrix_B)):
               matrix_C[i][j] += matrix_A[i][k] * matrix_B[k][j]  
    return matrix_C

# Strassen divide and conquer recursive algorithm 
def strassen(matrix_A, matrix_B):
    
    current_length = len(matrix_A)

    # Use a simpler algorithm the matrix height/width is under the recursion threshold
    if current_length <= LEAF_SIZE:
        return conventionnalProduct(matrix_A, matrix_B)
    else:
        # 1) initializing the 4 new sub-matrices with the 0 value
        new_length = int(current_length/2)
        a11 = [[0 for j in range(0, new_length)] for i in range(0, new_length)]
        a12 = [[0 for j in range(0, new_length)] for i in range(0, new_length)]
        a21 = [[0 for j in range(0, new_length)] for i in range(0, new_length)]
        a22 = [[0 for j in range(0, new_length)] for i in range(0, new_length)]

        b11 = [[0 for j in range(0, new_length)] for i in range(0, new_length)]
        b12 = [[0 for j in range(0, new_length)] for i in range(0, new_length)]
        b21 = [[0 for j in range(0, new_length)] for i in range(0, new_length)]
        b22 = [[0 for j in range(0, new_length)] for i in range(0, new_length)]

        a_middle_result = [[0 for j in range(0, new_length)] for i in range(0, new_length)]
        b_middle_result = [[0 for j in range(0, new_length)] for i in range(0, new_length)]

        # 2) dividing the original matrices in the 4 new sub-matrices:
        for i in range(0, new_length):
            for j in range(0, new_length):
                a11[i][j] = matrix_A[i][j]                     # top left
                a12[i][j] = matrix_A[i][j + new_length]           # top right
                a21[i][j] = matrix_A[i + new_length][j]           # bottom left
                a22[i][j] = matrix_A[i + new_length][j + new_length] # bottom right

                b11[i][j] = matrix_B[i][j]                     # top left
                b12[i][j] = matrix_B[i][j + new_length]           # top right
                b21[i][j] = matrix_B[i + new_length][j]           # bottom left
                b22[i][j] = matrix_B[i + new_length][j + new_length] # bottom right

        # 3) Calculation of p1 to p7 (according to the principles of the algorithm):
        
        a_middle_result = add(a11, a22)
        b_middle_result = add(b11, b22)
        p1 = strassen(a_middle_result, b_middle_result) # p1 = (a11+a22) * (b11+b22)

        a_middle_result = add(a21, a22)      # a21 + a22
        p2 = strassen(a_middle_result, b11)  # p2 = (a21+a22) * (b11)

        b_middle_result = subtract(b12, b22) # b12 - b22
        p3 = strassen(a11, b_middle_result)  # p3 = (a11) * (b12 - b22)

        b_middle_result = subtract(b21, b11) # b21 - b11
        p4 =strassen(a22, b_middle_result)   # p4 = (a22) * (b21 - b11)

        a_middle_result = add(a11, a12)      # a11 + a12
        p5 = strassen(a_middle_result, b22)  # p5 = (a11+a12) * (b22)   

        a_middle_result = subtract(a21, a11)    # a21 - a11
        b_middle_result = add(b11, b12)         # b11 + b12
        p6 = strassen(a_middle_result, b_middle_result) # p6 = (a21-a11) * (b11+b12)

        a_middle_result = subtract(a12, a22)    # a12 - a22
        b_middle_result = add(b21, b22)         # b21 + b22
        p7 = strassen(a_middle_result, b_middle_result) # p7 = (a12-a22) * (b21+b22)

        # 4) Calculation of c11, c12, c21 and of c22:
        c12 = add(p3, p5) # c12 = p3 + p5
        c21 = add(p2, p4)  # c21 = p2 + p4

        a_middle_result = add(p1, p4) # p1 + p4
        b_middle_result = add(a_middle_result, p7) # p1 + p4 + p7
        c11 = subtract(b_middle_result, p5) # c11 = p1 + p4 - p5 + p7

        a_middle_result = add(p1, p3) # p1 + p3
        b_middle_result = add(a_middle_result, p6) # p1 + p3 + p6
        c22 = subtract(b_middle_result, p2) # c22 = p1 + p3 - p2 + p6

        # 5) Grouping of the c_(i,j) results in a single matrix:
        matrix_C = [[0 for j in range(0, current_length)] for i in range(0, current_length)]
        for i in range(0, new_length):
            for j in range(0, new_length):
                matrix_C[i][j] = c11[i][j]
                matrix_C[i][j + new_length] = c12[i][j]
                matrix_C[i + new_length][j] = c21[i][j]
                matrix_C[i + new_length][j + new_length] = c22[i][j]
        return matrix_C

def runStrassen(file_nameA, file_nameB):
    
    # Extract matrix_A and matrix_B from the files
    matrix_A = extractMatrix(file_nameA)
    matrix_B = extractMatrix(file_nameB)
    
    # Sizes and types must be equals to perform a multiplication
    assert type(matrix_A) == list and type(matrix_B) == list
    assert len(matrix_A) == len(matrix_A[0]) == len(matrix_B) == len(matrix_B[0])

    # Make the matrix operation easier by creating even sized
    # matrices. This is possible by making the matrices larger,
    # using the next power of 2.
    nextPowerOfTwo = lambda n: 2**int(ceil(log(n,2)))
    current_length = len(matrix_A)
    next_power_length = nextPowerOfTwo(current_length)
    
    # Initialization of copies of old matrices for calculations
    APrep = [[0 for i in range(next_power_length)] for j in range(next_power_length)]
    BPrep = [[0 for i in range(next_power_length)] for j in range(next_power_length)]
    for i in range(current_length):
        for j in range(current_length):
            APrep[i][j] = matrix_A[i][j]
            BPrep[i][j] = matrix_B[i][j]
           
    # Start time count
    start_time = time.time()
            
    # Run Strassen algorithm
    CPrep = strassen(APrep, BPrep)
    
    # End time count
    global runtime
    end_time = time.time()
    runtime = end_time - start_time
    
    # Copy the result in a correctly sized matrix
    matrix_C = [[0 for i in range(current_length)] for j in range(current_length)]
    for i in range(current_length):
        for j in range(current_length):
            matrix_C[i][j] = CPrep[i][j]
            
    return matrix_C

def printMatrix(matrix):
    # Obtain the N
    file = open(ex_path1, 'r')
    N = int(file.readline())
    file.close()
    
    # Output of the requested format
    print(N)
    for line in matrix:
        print("\t".join(map(str,line)))
# Run the strassen algorithm
result = runStrassen(ex_path1, ex_path2)

# Call options (interface du laboratoire)
options = sys.argv[3:]
if '-p' in options: # Print result
    printMatrix(result)
if '-t' in options: # Print execution time
    print(runtime)
    