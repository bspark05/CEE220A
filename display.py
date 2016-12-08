'''
Created on Nov 24, 2016

@author: Administrator
'''
import numpy as np

np.set_printoptions(precision=3, suppress=True)

def format__1(digits,num):
    if digits<len(str(num)):
        raise Exception("digits<len(str(num))")
    return ' '*(digits-len(str(num))) + str(num)

def flattenList(list_of_lists):
    flattened = [val for sublist in list_of_lists for val in sublist]
    return flattened

def printmat(arr,row_labels=[], col_labels=[]): #print a 2d numpy array (maybe) or nested list
    arr = np.round(arr, 3)
    max_chars = max([len(str(item)) for item in flattenList(arr)+col_labels]) #the maximum number of chars required to display any item in list
    if row_labels==[] and col_labels==[]:
        for row in arr:
            print '[%s]' %(' '.join(format__1(max_chars,i) for i in row))
    elif row_labels!=[] and col_labels!=[]:
        rw = max([len(str(item)) for item in row_labels]) #max char width of row__labels
        print '%s %s' % (' '*(rw+1), ' '.join(format__1(max_chars,i) for i in col_labels))
        for row_label, row in zip(row_labels, arr):
            print '%s [%s]' % (format__1(rw,row_label), ' '.join(format__1(max_chars,i) for i in row))
    else:
        raise Exception("This case is not implemented...either both row_labels and col_labels must be given or neither.")
    
