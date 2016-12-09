# CEE220A Project Library

----------

## Description
This library is written in Python and intended to conduct a set of exercise in CEE220A 2016 Fall.

## Requirements
numpy, xlrd, scipy

## CEE220A library modules
* CEE220A.excel
* CEE220A.display
* CEE220A.TripGeneration.Production
* CEE220A.TripGeneration.Attraction
* CEE220A.TripDistribution.GravityModel
* CEE220A.Ex_1
* CEE220A.Ex2_1

## Function List 
### CEE220A.excel.excelRead
CEE220A.excel.**excelRead**(*filepath, sheetname*)
  : Read an excel file (.xlsx) and convert the cell values in a 2D list.

Parameters: | |
------|------
**filepath**|*string*
 | The path of a excel file including the file format
**sheetname**|*string*
 | The name of the worksheet of the excel file
 | |
**Returns:** | |
**excelList**|*list* 
 | A 2D list including all the cell values in the excel file

### CEE220A.excel.excelToArray
CEE220A.excel.**excelToArray**(*filepath, sheetname*)
  : Convert an excel list to numpy array format
  
Parameters: | |
------|------
**filepath**|*string*
 | The path of a excel file including the file format
**sheetname**|*string*
 | The name of the worksheet of the excel file
 | |
**Returns:** | |
**excelArray**|*numpy.ndarray* 
 | A multidimensional (n x m) array (where, n is the number of variables, m is the number of observations
 
### CEE283.jacobi_eigenvalue.maxelem
CEE283.jacobi_eigenvalue.**maxelem**(*matrix*)
: The maximum value and indices of the off-diagonal element in 2D array matrix

Parameters: | |
------|------
**matrix**|*numpy.ndarray*
 | A covariance matrix or correlation matrix to calculate the eigenvalues and corresponding eigenvectors
 | |
**Returns:** | |
**amax**|*numpy.float64* 
 | The maximum value
**ith**|*int* 
 | The row index of the maximum element
**jth**|*int* 
 | The column index of the maximum element
