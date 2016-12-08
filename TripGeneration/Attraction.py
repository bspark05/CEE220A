import numpy as np
import excel as ex
import display as dp
import scipy.stats as stats
import TripGeneration

filename = "CEE220A_Survey_Data.xlsx"

class Attraction():
    def __init__(self):
        np.set_printoptions(precision=3, suppress=True)
    
        self.busAttraction = self.tripsByAlternative("Attraction Current", "Bus")
        self.carAttraction = self.tripsByAlternative("Attraction Current", "Car")
        self.currentPop = np.array([20000, 10000, 30000, 5000])
        self.futurePop = np.array([30000, 15000, 45000, 10000])
        self.avgHHSize = [5.5, 3, 4.5, 2.5]
        
    def tripsByAlternative(self, attr, alt):
        attrRec = ex.excelRead(filename, attr)
        col_label = []
        for col in attrRec[0][1:]:
            col_label.append(str(col.value))
        
        row_label = ['zone1', 'zone2', 'zone3', 'zone4']
        
        attrArr = ex.excelToArray(filename, attr)
        if alt == "Bus":
            busArr = np.c_[attrArr[:,1], attrArr[:,3:]]
            busColLabel = [col_label[0]]+col_label[2:]
            return (busArr, row_label, busColLabel)
        elif alt == "Car":
            carArr = np.c_[attrArr[:,2:]]
            carColLabel = col_label[1:]
            return (carArr, row_label, carColLabel)
        else:
            print "select either 'Car' or 'Bus'."
            return None
    
    def varAltModel(self, alt, model):
        if alt == "Bus":
            if model == 0:
                idvBus = self.busAttraction[0][:, 1:]
                dvBus = self.busAttraction[0][:,0:1]
                
                colLabel = self.busAttraction[2][1:]
                return (np.log(dvBus), np.log(idvBus), colLabel)
                
            elif model == 1: 
                idvBus = np.c_[self.busAttraction[0][:, 1], self.busAttraction[0][:, 3:]]
                dvBus = self.busAttraction[0][:,0:1]
                
                colLabel = [self.busAttraction[2][1]]+self.busAttraction[2][3:]
                return (np.log(dvBus), np.log(idvBus), colLabel)
        
        elif alt=="Car":
            if model == 0:
                idvCar = self.carAttraction[0][:, 1:]
                dvCar = self.carAttraction[0][:, 0:1]
                
                colLabel = self.carAttraction[2][1:]
                return (np.log(dvCar), np.log(idvCar), colLabel)
            elif model == 1:
                idvCar = np.c_[self.carAttraction[0][:, 1], self.carAttraction[0][:, 3:]]
                dvCar = self.carAttraction[0][:, 0:1]
                
                colLabel = [self.carAttraction[2][1]]+self.carAttraction[2][3:]
                return (np.log(dvCar), np.log(idvCar), colLabel)
        
attr = Attraction()

    
def PrintBusAttraction():
    dp.printmat(attr.busAttraction[0], row_labels=attr.busAttraction[1], col_labels=attr.busAttraction[2])
    
def PrintCarAttraction():
    dp.printmat(attr.carAttraction[0], row_labels=attr.carAttraction[1], col_labels=attr.carAttraction[2])
    
def correlationMat(matrix):
    corrMat = np.corrcoef(np.transpose(matrix))
    return corrMat


def printCorrMat(alt, model):
    var = attr.varAltModel(alt, model)
    
    dp.printmat(correlationMat(var[1]), row_labels=var[2], col_labels=var[2])
    
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


def dj(alt, model, time):
    var = attr.varAltModel(alt, model)
    
    yCoeff=var[0]
    zCoeff=var[1]
    beta = coefficient(yCoeff, zCoeff)
    beta[0][0] = np.exp(beta[0][0])
    
    if time == 0:
        z=np.exp(zCoeff)
        
    elif time == 1:
        forecastDemo = ex.excelToArray(filename, "Attraction Forecast")
        z = np.c_[forecastDemo[:,3], forecastDemo[:,5:]]
        
    val0 = beta[0][0]*np.ones((len(z),1))
    val1 = []
    for i in z[:, 0]:
        val1 = np.append(val1, i**beta[1][0])
    val2 = []
    for i in z[:, 1]:
        val2 = np.append(val2, i**beta[2][0])
    val3 = []
    for i in z[:, 2]:
        val3 = np.append(val3, i**beta[3][0])
    
    val1=np.atleast_2d(val1).T
    val2=np.atleast_2d(val2).T
    val3=np.atleast_2d(val3).T
    
    
    dj1 = np.multiply(val0, val1)
    dj2 = np.multiply(val2, val3)
    dj = np.multiply(dj1, dj2)

    return dj

def printCoefficient(alt, model):
    var = attr.varAltModel(alt, model)
    
    y=var[0]
    z=var[1]

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
    
    dp.printmat(resultArr, col_labels=["Beta_hat", "1/cii", "S_beta", "t-statistic", "p-value"], row_labels=["constant"] + var[2])
    
    print "number of samples: ", "%d" % len(y)
    print "r-squared: ", "%.3f" % r
    print "standard error: ", "%.3f" % stdErr
