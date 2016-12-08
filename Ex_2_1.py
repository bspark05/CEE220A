import excel as ex
import display as dp
import numpy as np
import scipy.stats as stats

filename = "CEE220A_Survey_Data.xlsx"



class Ex_2_1():
    
    def __init__(self):
        np.set_printoptions(precision=3, suppress=True)
        
        self.HHRData = []
        self.HHRcolLabel = []
        self.HHRsheetname = "HH Record"
        
        ### Road the HH Record excel sheet
        HHRecord = ex.excelToArray(filename, self.HHRsheetname)
        self.HHRData = HHRecord[:,1:]
        
        ## define a column labels
        HHRecordList = ex.excelRead(filename, self.HHRsheetname)    
        colLabel2 = []
        for label in HHRecordList[0]:
            colLabel2.append(str(label.value))
        self.HHRcolLabel = colLabel2[1:]
        
         
        idv1= self.HHRData[:,2:]
        dv = self.HHRData[:,1:2]
        self.idv_model1 = idv1
        self.dv_model1 = dv
        
#         label2 = self.HHRcolLabel[2:3]
#         label2.extend(self.HHRData[4:6])
        label2 = self.HHRcolLabel[2:5]
        label2.extend(self.HHRcolLabel[7:])
        self.label2 = label2
#         idv2 = np.c_[self.HHRData[:,2:3], self.HHRData[:,4:6] ,self.HHRData[:,7:]]
        rmIdx = self.removeZeroIdx(dv)
        idv2 = np.c_[self.HHRData[:,2:5],self.HHRData[:,7:]]
        idv2rm = np.delete(idv2, rmIdx, axis=0)
#         idv2 = self.replaceValue(idv2, 0, 1)
        dv2rm = np.delete(dv, rmIdx, axis=0)
        self.idv_model2 = np.log(idv2rm)
        self.dv_model2 = np.log(dv2rm)
        
        idv3 = idv1
        idv3rm = np.delete(idv3, rmIdx, axis=0)
        dv3rm = np.delete(dv, rmIdx, axis=0)
        self.idv_model3 = idv3rm
        self.dv_model3 = np.log(dv3rm)
        
    def replaceValue(self, array, exist, replace):
        newArray = []
        for row in array:
            newRow = []
            for value in row:
                if value == exist:
                    value = replace
                newRow = np.append(newRow, value)
            if newArray == []:
                newArray = newRow
            else: 
                newArray = np.vstack((newArray, newRow))
        return newArray
    
    def removeZeroIdx(self, dv):
        idxList = []
        for idx, value in enumerate(dv):
            if value == 0:
                idxList.append(idx)
        return idxList                     
            
    
ex2_1 = Ex_2_1()

def correlationMat(matrix):
    corrMat = np.corrcoef(np.transpose(matrix))
    return corrMat



def printCorrMatModel1():
    dp.printmat(correlationMat(ex2_1.idv_model1), row_labels=ex2_1.HHRcolLabel[2:], col_labels=ex2_1.HHRcolLabel[2:])

def printCorrMatModel2():
    idvM2 = ex2_1.idv_model2
    dp.printmat(correlationMat(idvM2), row_labels=ex2_1.label2, col_labels=ex2_1.label2)

def printCorrMatModel3():
    dp.printmat(correlationMat(ex2_1.idv_model3), row_labels=ex2_1.HHRcolLabel[2:], col_labels=ex2_1.HHRcolLabel[2:])
    
def coefficient(y, z):
    z = np.insert(z,0,1, axis=1)
    zT = np.transpose(z)
    zTz = np.dot(zT, z)
    zTz_1 = np.linalg.inv(zTz)
    zTz_1zT = np.dot(zTz_1, zT)
    beta = np.dot(zTz_1zT, y)
    
    return beta

def cjj(zTz_1):
    cjj = []
    ind = 0
    while ind < len(zTz_1):
        cjj=np.append(cjj, zTz_1[ind][ind])
        ind+=1
    return np.reshape(cjj, (len(cjj), 1))

def stdError(beta, z, y, n, p):
    yhat = np.dot(z, beta)
    y_yhat = y-yhat
    y_yhat2 = np.multiply(y_yhat, y_yhat)
    y_yhat2Sum = np.sum(y_yhat2)
    stdErr = np.sqrt(y_yhat2Sum/(n-p-1))
    return stdErr

def s_beta(cjj, stdErr):
    sqrtCjj = np.sqrt(cjj)
    s_beta = sqrtCjj*stdErr
    return np.reshape(s_beta, (len(s_beta),1)) 

def t_test(beta, s_beta):   
    tStats = np.multiply(beta, 1/s_beta)
    return tStats

def p_value(tStats, df):
    p_values = stats.t.sf(np.abs(tStats), df)*2
    return p_values

def rSquared(beta, z, y):
    yhat = np.dot(z, beta)
    y_yhat = y-yhat
    y_yhat2 = np.multiply(y_yhat, y_yhat)
    y_yhat2Sum = np.sum(y_yhat2)
    
    yavg = np.mean(y)
    y_yavg = y-yavg
    y_yavg2 = np.multiply(y_yavg, y_yavg)
    y_yavg2Sum = np.sum(y_yavg2)
    
    r = 1-y_yhat2Sum/y_yavg2Sum
    return r

def printCoefficientModel1():
    y=ex2_1.dv_model1
    z=ex2_1.idv_model1
    beta = coefficient(y, z)
    
    z = np.insert(z,0,1, axis=1)
    zT = np.transpose(z)
    zTz = np.dot(zT, z)
    zTz_1 = np.linalg.inv(zTz)
    cjjList = cjj(zTz_1)
    
    stdErr = stdError(beta, z, y, len(y), len(beta))
    
    s_betaArr = s_beta(cjjList, stdErr)
    
    tStats = t_test(beta, s_betaArr)
    pValue = p_value(tStats, len(y)-len(beta)-1)
    
    resultArr = np.c_[(beta, cjjList, s_betaArr, tStats, pValue)]
    
    r = rSquared(beta, z, y)
    
    dp.printmat(resultArr, col_labels=["Beta_hat", "1/cii", "S_beta", "t-statistic", "p-value"], row_labels=["X0", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8"])
    
    print "r-squared: ", "%.3f" % r
    print "standard error: ", "%.3f" % stdErr 

def printCoefficientModel2():
    y=ex2_1.dv_model2
    z=ex2_1.idv_model2
    beta = coefficient(y, z)
    
    z = np.insert(z,0,1, axis=1)
    zT = np.transpose(z)
    zTz = np.dot(zT, z)
    zTz_1 = np.linalg.inv(zTz)
    cjjList = cjj(zTz_1)
    
    stdErr = stdError(beta, z, y, len(y), len(beta))
    
    s_betaArr = s_beta(cjjList, stdErr)
    
    tStats = t_test(beta, s_betaArr)
    pValue = p_value(tStats, len(y)-len(beta)-1)
    
    resultArr = np.c_[(beta, cjjList, s_betaArr, tStats, pValue)]
    
    r = rSquared(beta, z, y)
    
    dp.printmat(resultArr, col_labels=["Beta_hat", "1/cii", "S_beta", "t-statistic", "p-value"], row_labels=["X0", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8"])
    
    print "r-squared: ", "%.3f" % r
    print "standard error: ", "%.3f" % stdErr
    
def printCoefficientModel3():
    y=ex2_1.dv_model3
    z=ex2_1.idv_model3
    beta = coefficient(y, z)
    
    z = np.insert(z,0,1, axis=1)
    zT = np.transpose(z)
    zTz = np.dot(zT, z)
    zTz_1 = np.linalg.inv(zTz)
    cjjList = cjj(zTz_1)
    
    stdErr = stdError(beta, z, y, len(y), len(beta))
    
    s_betaArr = s_beta(cjjList, stdErr)
    
    tStats = t_test(beta, s_betaArr)
    pValue = p_value(tStats, len(y)-len(beta)-1)
    
    resultArr = np.c_[(beta, cjjList, s_betaArr, tStats, pValue)]
    
    r = rSquared(beta, z, y)
    
    dp.printmat(resultArr, col_labels=["Beta_hat", "1/cii", "S_beta", "t-statistic", "p-value"], row_labels=["X0", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8"])

    print "r-squared: ", "%.3f" % r
    print "standard error: ", "%.3f" % stdErr


