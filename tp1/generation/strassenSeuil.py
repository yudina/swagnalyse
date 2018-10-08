# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 11:46:48 2018

@author: kevin
"""

from optparse import OptionParser
from math import ceil, log
import time
import csv

global times
times = []

def extractMatrix(fileName):
    newMatrix = []
    
    with open(fileName,'r') as f1:
        for line in f1:
            line = line.strip()
            if len(line) > 1:
               newMatrix.append([int(a) for a in line.split()])
    return newMatrix

# The simple algorithm used under the leaf_size value (recursion threshold)
def conventionnalProduct(matrixA, matrixB):    
    
    # matrix initialization
    w, h = len(matrixA[0]), len(matrixB[0]);
    matrixC = [[0 for x in range(w)] for y in range(h)]
    
    for i in range(len(matrixA)):
       # iterate through columns of Y
       for j in range(len(matrixB[0])):
           # iterate through rows of Y
           for k in range(len(matrixB)):
               matrixC[i][j] += matrixA[i][k] * matrixB[k][j]  
    return matrixC

# Make an algebric addition of 2 same dimensions matrices
def add(matrixA, matrixB):
    
    # matrix initialization
    length = len(matrixA)
    matrixC = [[0 for j in range(0, length)] for i in range(0, length)]
    
    # addition on each element
    for i in range(0, length):
        for j in range(0, length):
            matrixC[i][j] = matrixA[i][j] + matrixB[i][j]
    return matrixC

# Make an algebric substraction of 2 same dimensions matrices
def subtract(matrixA, matrixB):
    
    # matrix initialization
    length = len(matrixA)
    matrixC = [[0 for j in range(0, length)] for i in range(0, length)]
    
    # substraction on each element
    for i in range(0, length):
        for j in range(0, length):
            matrixC[i][j] = matrixA[i][j] - matrixB[i][j]
    return matrixC

# Strassen divide and conquer recursive algorithm 
def strassen(matrixA, matrixB):
    
    currentLength = len(matrixA)

    # Use a simpler algorithm the matrix height/width is under the recursion threshold
    if currentLength <= LEAF_SIZE:
        return conventionnalProduct(matrixA, matrixB)
    else:
        # 1) initializing the 4 new sub-matrices with the 0 value
        newLength = int(currentLength/2)
        a11 = [[0 for j in range(0, newLength)] for i in range(0, newLength)]
        a12 = [[0 for j in range(0, newLength)] for i in range(0, newLength)]
        a21 = [[0 for j in range(0, newLength)] for i in range(0, newLength)]
        a22 = [[0 for j in range(0, newLength)] for i in range(0, newLength)]

        b11 = [[0 for j in range(0, newLength)] for i in range(0, newLength)]
        b12 = [[0 for j in range(0, newLength)] for i in range(0, newLength)]
        b21 = [[0 for j in range(0, newLength)] for i in range(0, newLength)]
        b22 = [[0 for j in range(0, newLength)] for i in range(0, newLength)]

        a_middle_result = [[0 for j in range(0, newLength)] for i in range(0, newLength)]
        b_middle_result = [[0 for j in range(0, newLength)] for i in range(0, newLength)]

        # 2) dividing the original matrices in the 4 new sub-matrices:
        for i in range(0, newLength):
            for j in range(0, newLength):
                a11[i][j] = matrixA[i][j]                     # top left
                a12[i][j] = matrixA[i][j + newLength]           # top right
                a21[i][j] = matrixA[i + newLength][j]           # bottom left
                a22[i][j] = matrixA[i + newLength][j + newLength] # bottom right

                b11[i][j] = matrixB[i][j]                     # top left
                b12[i][j] = matrixB[i][j + newLength]           # top right
                b21[i][j] = matrixB[i + newLength][j]           # bottom left
                b22[i][j] = matrixB[i + newLength][j + newLength] # bottom right

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
        matrixC = [[0 for j in range(0, currentLength)] for i in range(0, currentLength)]
        for i in range(0, newLength):
            for j in range(0, newLength):
                matrixC[i][j] = c11[i][j]
                matrixC[i][j + newLength] = c12[i][j]
                matrixC[i + newLength][j] = c21[i][j]
                matrixC[i + newLength][j + newLength] = c22[i][j]
        return matrixC

def runStrassen(filenameA, filenameB):
    
    # Extract matrixA and matrixB from the files
    matrixA = extractMatrix(filenameA)
    matrixB = extractMatrix(filenameB)
    
    # Sizes and types must be equals to perform a multiplication
    assert type(matrixA) == list and type(matrixB) == list
    assert len(matrixA) == len(matrixA[0]) == len(matrixB) == len(matrixB[0])

    # Make the matrix operation easier by creating even sized
    # matrices. This is possible by making the matrices larger,
    # using the next power of 2.
    nextPowerOfTwo = lambda n: 2**int(ceil(log(n,2)))
    currentLength = len(matrixA)
    nextPowerLength = nextPowerOfTwo(currentLength)
    
    # Initialization of copies of old matrices for calculations
    APrep = [[0 for i in range(nextPowerLength)] for j in range(nextPowerLength)]
    BPrep = [[0 for i in range(nextPowerLength)] for j in range(nextPowerLength)]
    for i in range(currentLength):
        for j in range(currentLength):
            APrep[i][j] = matrixA[i][j]
            BPrep[i][j] = matrixB[i][j]
            
    # Run Strassen algorithm
    CPrep = strassen(APrep, BPrep)
    
    # Copy the result in a correctly sized matrix
    matrixC = [[0 for i in range(currentLength)] for j in range(currentLength)]
    for i in range(currentLength):
        for j in range(currentLength):
            matrixC[i][j] = CPrep[i][j]
    print("result value is :")
    print(matrixC)
    return matrixC

if __name__ == "__main__":
    
    LEAF_SIZE = 1
    
    print("started strassen")
    main_start_time = time.time()
#    runStrassen("ex1.1","ex1.2")
#    runStrassen("ex1.1","ex1.3")
#    runStrassen("ex1.1","ex1.4")
#    runStrassen("ex1.1","ex1.5")
#    runStrassen("ex1.2","ex1.3")
#    runStrassen("ex1.2","ex1.4")
#    runStrassen("ex1.2","ex1.5")
#    runStrassen("ex1.3","ex1.4")
#    runStrassen("ex1.3","ex1.5")
#    runStrassen("ex1.4","ex1.5")
#    
    runStrassen("ex2.1","ex2.2")
#    runStrassen("ex2.1","ex2.3")
#    runStrassen("ex2.1","ex2.4")
#    runStrassen("ex2.1","ex2.5")
#    runStrassen("ex2.2","ex2.3")
#    runStrassen("ex2.2","ex2.4")
#    runStrassen("ex2.2","ex2.5")
#    runStrassen("ex2.3","ex2.4")
#    runStrassen("ex2.3","ex2.5")
#    runStrassen("ex2.4","ex2.5")
#    
#    runStrassen("ex3.1","ex3.2")
#    runStrassen("ex3.1","ex3.3")
#    runStrassen("ex3.1","ex3.4")
#    runStrassen("ex3.1","ex3.5")
#    runStrassen("ex3.2","ex3.3")
#    runStrassen("ex3.2","ex3.4")
#    runStrassen("ex3.2","ex3.5")
#    runStrassen("ex3.3","ex3.4")
#    runStrassen("ex3.3","ex3.5")
#    runStrassen("ex3.4","ex3.5")
#    
#    runStrassen("ex4.1","ex4.2")
#    runStrassen("ex4.1","ex4.3")
#    runStrassen("ex4.1","ex4.4")
#    runStrassen("ex4.1","ex4.5")
#    runStrassen("ex4.2","ex4.3")
#    runStrassen("ex4.2","ex4.4")
#    runStrassen("ex4.2","ex4.5")
#    runStrassen("ex4.3","ex4.4")
#    runStrassen("ex4.3","ex4.5")
#    runStrassen("ex4.4","ex4.5")
#    
#    runStrassen("ex5.1","ex5.2")
#    runStrassen("ex5.1","ex5.3")
#    runStrassen("ex5.1","ex5.4")
#    runStrassen("ex5.1","ex5.5")
#    runStrassen("ex5.2","ex5.3")
#    runStrassen("ex5.2","ex5.4")
#    runStrassen("ex5.2","ex5.5")
#    runStrassen("ex5.3","ex5.4")
#    runStrassen("ex5.3","ex5.5")
#    runStrassen("ex5.4","ex5.5")
    
    main_runtime = time.time() - main_start_time
    times.append(main_runtime)
    
    print(times)
    print("main_runtime : ")
    print(main_runtime)

csvfile = "outStrassen.csv"

#Assuming res is a flat list
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for t in times:
        writer.writerow([t])  
    
#    parser = OptionParser()
#    parser.add_option("-i", dest="filename", default="2000.in",
#         help="input file with two matrices", metavar="FILE")
#    parser.add_option("-l", dest="LEAF_SIZE", default="8",
#         help="when do you start using ikj", metavar="LEAF_SIZE")
#    (options, args) = parser.parse_args()
#
#    LEAF_SIZE = options.LEAF_SIZE
#    A, B = read(options.filename)
#
#    C = strassen(A, B)
#    print(C)

