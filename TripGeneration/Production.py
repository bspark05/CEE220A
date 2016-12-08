import numpy as np
import excel as ex
import display as dp
import scipy.stats as stats

filename = "CEE220A_Survey_Data.xlsx"

class Production():
    def __init__(self):
        np.set_printoptions(precision=3, suppress=True)
        
        self.busTripRecords = self.tripsByAlternative("Trip Record", "Bus")
        self.carTripRecords = self.tripsByAlternative("Trip Record", "Car")
        self.currentPop = np.array([20000, 10000, 30000, 5000])
        self.futurePop = np.array([30000, 15000, 45000, 10000])
        self.avgHHSize = [5.5, 3, 4.5, 2.5]
    
    def varAltModel(self, alt, model):
        
        if alt == "Bus":
            idvBus = self.busTripRecords[0][:,2:]
            dvBus = self.busTripRecords[0][:,1:2]
            zoneBus = self.busTripRecords[0][:,0]
            rmIdx = self.removeZeroIdx(dvBus)
            idvBusrm = np.delete(idvBus, rmIdx, axis=0)
            dvBusrm = np.delete(dvBus, rmIdx, axis=0)
            zoneBusrm = np.delete(zoneBus, rmIdx, axis=0)
            colLabel = self.busTripRecords[2][2:]        
            colLabel2 = self.busTripRecords[2][2:5] + self.busTripRecords[2][7:]
            idvBus2 = np.c_[self.busTripRecords[0][:,2:5],self.busTripRecords[0][:,7:]]
            idvBusrm2 = np.delete(idvBus2, rmIdx, axis=0)
                    
            if model == 1:
                
                return (dvBus, idvBus, colLabel, zoneBus)
            
            if model == 2:
                
                return (np.log(dvBusrm), np.log(idvBusrm2), colLabel2, zoneBusrm)
            
            if model == 3:
                return (np.log(dvBusrm), idvBusrm, colLabel, zoneBusrm)
            
            
        if alt == "Car":
            idvCar = self.carTripRecords[0][:,2:]
            dvCar = self.carTripRecords[0][:,1:2]
            zoneCar = self.carTripRecords[0][:,0]
            rmIdx = self.removeZeroIdx(dvCar)
            idvCarrm = np.delete(idvCar, rmIdx, axis=0)
            dvCarrm = np.delete(dvCar, rmIdx, axis=0)
            zoneCarrm = np.delete(zoneCar, rmIdx, axis=0)
            colLabel = self.carTripRecords[2][2:]
            colLabel2 = self.carTripRecords[2][2:5] + self.carTripRecords[2][7:]
            idvCar2 = np.c_[self.carTripRecords[0][:,2:5],self.carTripRecords[0][:,7:]]
            idvCarrm2 = np.delete(idvCar2, rmIdx, axis=0)
            if model == 1:
                return (dvCar, idvCar, colLabel, zoneCar)
            
            if model == 2:
                return (np.log(dvCarrm), np.log(idvCarrm2), colLabel2, zoneCarrm)
            
            if model == 3:
                
                return (np.log(dvCarrm), idvCarrm, colLabel, zoneCarrm)
            
            
    def tripsByAlternative(self, trip, alt):
        tripRec = ex.excelRead(filename, trip)
        altInd = 0
        altList = []
        altTrips = 0.0
        for tripRow in tripRec[2:]:
            if tripRow[3].ctype == 2:
                altInd += 1
                tripRow[5].value=np.log10(float(tripRow[5].value))
                tripRow[9].value=np.log10(float(tripRow[9].value))
                altList.append(tripRow)
                if altInd >= 2:
                    altList[altInd-2][2].value = altTrips
                    altTrips = 0.0
            
            if str(tripRow[3].value) == alt:
                altTrips += 1
        
        varList = []
        # first row is a field name
        for row in altList:
            rowList = []
            for value in row:
                rowList.append(float(value.value))
            varList.append(rowList)
        varArray = np.array(varList)
        
        arr = varArray[:,1:]
        
        rowLabel = varArray[:,0]
        
        colLabel = []
        for col in tripRec[0][1:]:
            colLabel.append(str(col.value))
        
        return (arr, rowLabel, colLabel)
                
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
        
prod = Production()

    
def PrintBusTripRecord():
    dp.printmat(prod.busTripRecords[0], row_labels=prod.busTripRecords[1], col_labels=prod.busTripRecords[2])
    
def PrintCarTripRecord():
    dp.printmat(prod.carTripRecords[0], row_labels=prod.carTripRecords[1], col_labels=prod.carTripRecords[2])

def correlationMat(matrix):
    corrMat = np.corrcoef(np.transpose(matrix))
    return corrMat


def printCorrMat(alt, model):
    var = prod.varAltModel(alt, model)
    
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

def oi(alt, model, time):
    if time == 0:
        pop = prod.currentPop
        
    elif time == 1:
        pop = prod.futurePop
    
    avgHHsize_1 = []
    for i in prod.avgHHSize:
        avgHHsize_1=np.append(avgHHsize_1, 1/float(i))    
    
    hh= np.multiply(pop,avgHHsize_1) 
    
    var = prod.varAltModel(alt, model)
    
    y=var[0]
    z=var[1]
    zone = var[3]
        
    beta = coefficient(y, z)
    obs = np.insert(z, [0], [1], axis=1)
    yhat = np.dot(obs, beta)
#     print zone
    yhatZone1 = []
    yhatZone2 = []
    yhatZone3 = []
    yhatZone4 = []
    ind=0
    for yh in yhat:
        if zone[ind] == 1.:
            yhatZone1 = np.append(yhatZone1, yh)
        elif zone[ind] == 2.:
            yhatZone2 = np.append(yhatZone2, yh)
        elif zone[ind] == 3.:
            yhatZone3 = np.append(yhatZone3, yh)
        elif zone[ind] == 4.:
            yhatZone4 = np.append(yhatZone4, yh)
        ind+=1
    
    yhatZone = np.array([np.average(yhatZone1), np.average(yhatZone2), np.average(yhatZone3), np.average(yhatZone4)])
    oi = np.multiply(hh, yhatZone)
    oi = np.atleast_2d(oi).T
    return oi

def printCoefficient(alt, model):
    var = prod.varAltModel(alt, model)
    
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
    
def PrintCoefficient2(alt, model):
    var = prod.varAltModel(alt, model)
    
    y=var[0]
    z=var[1]
    
    label = var[2]
    beta = coefficient(y, z)
    
    z = np.insert(z,0,1, axis=1)
    zT = np.transpose(z)
    zTz = np.dot(zT, z)
    zTz_1 = np.linalg.inv(zTz)
    cjjList = cjj(zTz_1)
    
    stdErr = stdError(beta, z, y, len(y), len(beta))
    
    s_betaArr = s_beta(cjjList, stdErr)
    
    tStats = t_test(beta, s_betaArr)
    
    z2List = []
    z2label = []
    for ind, val in enumerate(tStats[1:]):
        if val >= 1.645 or val <= -1.645:
            z2List.append(z[:,ind+1])
            
#             if ind >0:
            z2label.append(label[ind])
    
    i=1
    z2 = z2List[0]
    while i <= len(z2List)-1:
        z2 = np.vstack((z2, z2List[i]))
        i+=1
    
    z2 = np.transpose(z2)
#     print z2
    beta2 = coefficient(y, z2)
    
    z2 = np.insert(z2,0,1, axis=1)
    zT2 = np.transpose(z2)
    zTz2 = np.dot(zT2, z2)
    zTz_12 = np.linalg.inv(zTz2)
    cjjList2 = cjj(zTz_12)
    
    stdErr2 = stdError(beta2, z2, y, len(y), len(beta2))
    
    s_betaArr2 = s_beta(cjjList2, stdErr2)
    
    tStats2 = t_test(beta2, s_betaArr2)
    pValue2 = p_value(tStats2, len(y)-len(beta2)-1)
    
    resultArr2 = np.c_[(beta2, cjjList2, s_betaArr2, tStats2, pValue2)]
    
    r2 = rSquared(beta2, z2, y)
    
    dp.printmat(resultArr2, col_labels=["Beta_hat", "1/cii", "S_beta", "t-statistic", "p-value"], row_labels=["constant"] + z2label)
    
    print "number of samples: ", "%d" % len(y)
    print "r-squared: ", "%.3f" % r2
    print "standard error: ", "%.3f" % stdErr2
        