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

### CEE220A.display.printmat
CEE220A.display.**printmat**(*arr, row_labels, col_labels*)
  : Visualization for an array with labels

Parameters: | |
------|------
**arr**|*numpy.ndarray*
 | An array to visualize
**row_labels**|*list*
 | labels for rows
**col_labels**|*list*
 | labels for columns
 
### CEE220A.TripGeneration.Production.correlationMat
CEE220A.TripGeneration.Production.**correlationMat**(*matrix*)
  : Caculation of correlation matrix of the input matrix

Parameters: | |
------|------
**matrix**|*numpy.ndarray*
 | An array of observations
 | |
**Returns:** | |
**corrMat**|*numpy.ndarray*
 | correlation matrix of the observations

### CEE220A.TripGeneration.Production.coefficient
CEE220A.TripGeneration.Production.**coefficient**(*y, z*)
: Caculation of a set of coefficients of a linear regression model

Parameters: | |
------|------
**y**|*numpy.ndarray*
 | Observations of the dependent variable
**z**|*numpy.ndarray*
 | Observations of explanatory variables
 | |
**Returns:** | |
**beta**|*numpy.ndarray*
 | A set of coefficients of the model

### CEE220A.TripGeneration.Production.stdError
CEE220A.TripGeneration.Production.**stdError**(*beta, z, y, n, p*)
: Caculation of the standard error of a model

Parameters: | |
------|------
**beta**|*numpy.ndarray*
 | A set of coefficients of the model
**z**|*numpy.ndarray*
 | Observations of explanatory variables
**y**|*numpy.ndarray*
 | Observations of the dependent variable
**n**|*int*
 | The number of observations
**p**|*int*
 | The number of explanatory variables
 | |
**Returns:** | |
**stdErr**|*float*
 | The value of standard error of the model

### CEE220A.TripGeneration.Production.t_test
CEE220A.TripGeneration.Production.**t_test**(*beta, s_beta*)
: Caculation of the t statistics of each variable

Parameters: | |
------|------
**beta**|*numpy.ndarray*
 | A set of coefficients of the model
**s_beta**|*numpy.ndarray*
 | Standard error of estimated coefficients
 | |
**Returns:** | |
**tStat**|*numpy.ndarray*
 | A set of t statistics of the estimated coefficients
 
### CEE220A.TripGeneration.Production.p_value
CEE220A.TripGeneration.Production.**p_value**(*tStats, df*)
: Caculation of the p values of the corresponding  t values in the degree of freedom df

Parameters: | |
------|------
**tStat**|*numpy.ndarray*
 | A set of t statistics of the estimated coefficients
**df**|*int*
 | A degree of freedom of the model
 | |
**Returns:** | |
**p_values**|*numpy.ndarray*
 | A set of p values

### CEE220A.TripGeneration.Production.rSquared
CEE220A.TripGeneration.Production.**rSquared**(*beta, z, y*)
: Caculation of the r-squared value of a model

Parameters: | |
------|------
**beta**|*numpy.ndarray*
 | A set of coefficients of the model
**z**|*numpy.ndarray*
 | Observations of explanatory variables
**y**|*numpy.ndarray*
 | Observations of the dependent variable
 | |
**Returns:** | |
**r**|*float*
 | The r-squared value of the model

### CEE220A.TripGeneration.Production.oi
CEE220A.TripGeneration.Production.**oi**(*alt, model, time*)
: Estimation of Oi for each zone for an alternative

Parameters: | |
------|------
**alt**|*string*
 | An alternative, Bus or Car
**model**|*int*
 | A model number/ 1: Linear form, 2: Multiplicative form, 3: Exponential form
**time**|*int*
 | An index of estimation time/ 1: base year, 2: year of 2030
 | |
**Returns:** | |
**oi**|*numpy.ndarray*
 | Estimatted Oi for each zone

### CEE220A.TripGeneration.Attraction.dj
CEE220A.TripGeneration.Attraction.**dj**(*alt, model, time*)
: Estimation of Dj for each zone for an alternative

Parameters: | |
------|------
**alt**|*string*
 | An alternative, Bus or Car
**model**|*int*
 | A model number/ 1: Linear form, 2: Multiplicative form, 3: Exponential form
**time**|*int*
 | An index of estimation time/ 1: base year, 2: year of 2030
 | |
**Returns:** | |
**dj**|*numpy.ndarray*
 | Estimatted Dj for each zone

### CEE220A.TripDistribution.GravityModel.adjDjF
CEE220A.TripDistribution.GravityModel.**adjDjF**(*oi, dj*)
: Matching operation of Dj's based on Oi's

Parameters: | |
------|------
**oi**|*numpy.ndarray*
 | Estimated Oi's in the trip production process
**dj**|*numpy.ndarray*
 | Estimated Dj's in the trip attraction process
 | |
**Returns:** | |
**adjDj**|*numpy.ndarray*
 | Adjusted Dj's based on Oi's

### CEE220A.TripDistribution.GravityModel.calcBar
CEE220A.TripDistribution.GravityModel.**calcBar**(*tij, cij*)
: Calculation of average cost(initial value)

Parameters: | |
------|------
**tij**|*numpy.ndarray*
 | Tij table from a survey data
**cij**|*numpy.ndarray*
 | Travel time table
 | |
**Returns:** | |
**cBar**|*float*
 | Initial value of c bar
 
### CEE220A.TripDistribution.GravityModel.iterationAB
CEE220A.TripDistribution.GravityModel.**iterationAB**(*tij, oi, dj, cij, mu, threshold*)
: Iteration process to figure out Ai's and Bj's until satisfying threshold condition

Parameters: | |
------|------
**tij**|*numpy.ndarray*
 | Tij table from a survey data
**oi**|*numpy.ndarray*
 | Estimated Oi's in the trip production process
**dj**|*numpy.ndarray*
 | Estimated Dj's in the trip attraction process
**cij**|*numpy.ndarray*
 | Travel time table
**mu**|*float*
 | mu value 
**threshold**|*float*
 | A value to determine further iteration process
 | |
**Returns:** | |
**aList**|*numpy.ndarray*
 | Ai list
**bList**|*numpy.ndarray*
 | Bj list

### CEE220A.TripDistribution.GravityModel.tijHat
CEE220A.TripDistribution.GravityModel.**tijHat**(*ai, bj, oi, dj, mu, cij*)
: Estimation of Tij hat based on a series of estimated values(ai, bj, oi, dj)

Parameters: | |
------|------
**ai**|*numpy.ndarray*
 | Ai's estimated
**bj**|*numpy.ndarray*
 | Bj's estimated
**oi**|*numpy.ndarray*
 | Estimated Oi's in the trip production process
**dj**|*numpy.ndarray*
 | Estimated Dj's in the trip attraction process
**mu**|*float*
 | mu value 
**cij**|*numpy.ndarray*
 | Travel time table
**threshold**|*float*
 | A value to determine further iteration process
 | |
**Returns:** | |
**tijHat**|*numpy.ndarray*
 | Estimated Tij table
