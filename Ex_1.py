import numpy as np
import excel as ex
import display as dp
import scipy.stats as stats

filename = "CEE220A_Survey_Data.xlsx"

class Ex_1():
    def __init__(self):
        np.set_printoptions(precision=3, suppress=True)
        
        self.CZDData = []
        self.CZDcolLabel = []
        self.CZDsheetname = "Current Zonal Demographics"
        
        ### Road the Current Zonal Demographics excel sheet
        currZoneDemo = ex.excelToArray(filename, self.CZDsheetname)
        self.CZDData = currZoneDemo[:,1:7]
        
        ## define a column labels
        currZoneDemoList = ex.excelRead(filename, self.CZDsheetname)    
        colLabel1 = []
        for label in currZoneDemoList[0]:
            colLabel1.append(str(label.value))
        self.CZDcolLabel = colLabel1[1:7]
        
        
        
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
    
        
        self.zone1 = []
        self.zone2 = []
        self.zone3 = []
        self.zone4 = []
        self.rowLabelZone1 = []
        self.rowLabelZone2 = []
        self.rowLabelZone3 = []
        self.rowLabelZone4 = []
        
        
        
        self.HHMean = []
        self.HHMeancolLabel=[]
        
        
        
        self.sampleMeanArray = []
        self.sampleStdArray = []
        self.sampleSize = []
        
        
        
        self.tStats = []
        self.pValues = []
        
ex1 = Ex_1()

def printCurrentZonalDemo():
    ## display the excel sheet
    dp.printmat(ex1.CZDData, col_labels=ex1.CZDcolLabel, row_labels=["Zone1", "Zone2", "Zone3", "Zone4"])

def printHHRecord():
    ## display the excel sheet
    dp.printmat(ex1.HHRData, col_labels=ex1.HHRcolLabel, row_labels=ex1.HHRecord[:,0])
    
def categorizeHHRecord():
    ### Categorize the dataset based on Home Zone
    zone1 = []
    zone2 = []
    zone3 = []
    zone4 = []
    rowLabelZone1 = []
    rowLabelZone2 = []
    rowLabelZone3 = []
    rowLabelZone4 = []
    
    for ind, hhrow in enumerate(ex1.HHRData):
        if hhrow[0] == 1:
            if zone1 == []:
                zone1 = hhrow
            else:
                zone1 = np.vstack((zone1, hhrow))
            rowLabelZone1.append(ind+1) 
                
        elif hhrow[0] == 2:
            if zone2 == []:
                zone2 = hhrow
            else:
                zone2 = np.vstack((zone2, hhrow))
            rowLabelZone2.append(ind+1)
            
        elif hhrow[0] == 3:
            if zone3 == []:
                zone3 = hhrow
            else:
                zone3 = np.vstack((zone3, hhrow))
            rowLabelZone3.append(ind+1)
                
        elif hhrow[0] == 4:
            if zone4 == []:
                zone4 = hhrow
            else:
                zone4 = np.vstack((zone4, hhrow))
            rowLabelZone4.append(ind+1)
            
    ex1.zone1= zone1
    ex1.zone2= zone2
    ex1.zone3= zone3
    ex1.zone4= zone4
    ex1.rowLabelZone1 = rowLabelZone1
    ex1.rowLabelZone2 = rowLabelZone2
    ex1.rowLabelZone3 = rowLabelZone3
    ex1.rowLabelZone4 = rowLabelZone4
    
    
def printHHRecordZones():
    categorizeHHRecord()
    
    print "Zone1:"
    dp.printmat(ex1.zone1, col_labels=ex1.HHRcolLabel, row_labels=ex1.rowLabelZone1)
    print "Zone2:"
    dp.printmat(ex1.zone2, col_labels=ex1.HHRcolLabel, row_labels=ex1.rowLabelZone2)
    print "Zone3:"
    dp.printmat(ex1.zone3, col_labels=ex1.HHRcolLabel, row_labels=ex1.rowLabelZone3)
    print "Zone4:"
    dp.printmat(ex1.zone4, col_labels=ex1.HHRcolLabel, row_labels=ex1.rowLabelZone4)
    
def HHMean():
    ### Calculate the average no of employed member per household
    CZDTrans = np.transpose(ex1.CZDData)
    empHHMem = CZDTrans[5,:]
    avgEmpMemHH = empHHMem / CZDTrans[1,:]
    
    ### HH Mean array
    HHMeanArray1 = np.c_[ex1.CZDData[:,4], avgEmpMemHH, ex1.CZDData[:,3]]
    
    ### Calculate the population mean
    meanArray = np.array([])
    
#         meanList.append(np.sum(CZDTrans[0]))
    
    totalHH = np.sum(CZDTrans[1])
#         meanList.append(totalHH)
    
#         meanList.append(np.sum(CZDTrans[2]))
    
    avgHHSize = np.sum(np.multiply(CZDTrans[1], CZDTrans[4])) / totalHH
    meanArray=np.append(meanArray, avgHHSize)
    
    avgEmpMem = np.sum(CZDTrans[5]) / totalHH
    meanArray=np.append(meanArray, avgEmpMem)
    
    avgHHInc = np.sum(np.multiply(CZDTrans[1], CZDTrans[3])) / totalHH
    meanArray=np.append(meanArray, avgHHInc)
    
    HHMeanArray2 = np.vstack((HHMeanArray1, meanArray))
    ex1.HHMean= HHMeanArray2
    ex1.HHMeancolLabel = [ex1.CZDcolLabel[4], "AVG_EMP_MEM", ex1.CZDcolLabel[3]]

def printHHMean():
    HHMean()
    
    dp.printmat(ex1.HHMean, row_labels=["Zone1", "Zone2", "Zone3", "Zone4", "Whole Region"], col_labels=ex1.HHMeancolLabel)

def sampleMean():
    categorizeHHRecord()
    zone1Data = ex1.zone1[:,2:5]
    zone2Data = ex1.zone2[:,2:5]
    zone3Data = ex1.zone3[:,2:5]
    zone4Data = ex1.zone4[:,2:5]
    HHRData = ex1.HHRData[:,2:5]
    
    sampleMeanArray = zone1Data.mean(0)
    sampleMeanArray = np.vstack((sampleMeanArray, zone2Data.mean(0)))
    sampleMeanArray = np.vstack((sampleMeanArray, zone3Data.mean(0)))
    sampleMeanArray = np.vstack((sampleMeanArray, zone4Data.mean(0)))
    sampleMeanArray = np.vstack((sampleMeanArray, HHRData.mean(0)))
    
    ex1.sampleMeanArray = sampleMeanArray

def printSampleMean():
    sampleMean()
    HHMean()
    dp.printmat(ex1.sampleMeanArray, row_labels = ["Zone1", "Zone2", "Zone3", "Zone4", "Whole Region"], col_labels = ex1.HHMeancolLabel)

def sampleStd():
    categorizeHHRecord()
    zone1Data = ex1.zone1[:,2:5]
    zone2Data = ex1.zone2[:,2:5]
    zone3Data = ex1.zone3[:,2:5]
    zone4Data = ex1.zone4[:,2:5]
    HHRData = ex1.HHRData[:,2:5]
    
    sampleStdArray = np.std(zone1Data, axis=0, ddof=1)
    sampleStdArray = np.vstack((sampleStdArray, np.std(zone2Data, axis=0, ddof=1)))
    sampleStdArray = np.vstack((sampleStdArray, np.std(zone3Data, axis=0, ddof=1)))
    sampleStdArray = np.vstack((sampleStdArray, np.std(zone4Data, axis=0, ddof=1)))
    sampleStdArray = np.vstack((sampleStdArray, np.std(HHRData, axis=0, ddof=1)))
     
    ex1.sampleStdArray = sampleStdArray
     
def printSampleStd():
    sampleStd()
    HHMean()
    
    dp.printmat(ex1.sampleStdArray, row_labels=["Zone1", "Zone2", "Zone3", "Zone4", "Whole Region"], col_labels=ex1.HHMeancolLabel)    

def sampleSize():
    ex1.sampleSize = np.array([[len(ex1.zone1)], [len(ex1.zone2)], [len(ex1.zone3)], [len(ex1.zone4)], [len(ex1.HHRData)]])

def printSampleSize():
    sampleSize()
    dp.printmat(ex1.sampleSize, row_labels=["Zone1", "Zone2", "Zone3", "Zone4", "Whole Region"], col_labels=["Sample Size"])
     
def t_test():
    HHMean()
    sampleMean()
    sampleStd()
    sampleSize()
    
    mu = ex1.HHMean
    m = ex1.sampleMeanArray
    s = ex1.sampleStdArray
    n = ex1.sampleSize
    
    t1 = (m - mu)
    t2 = np.sqrt(n)
    t3 = np.multiply(t1, t2)
    t_stats = np.divide(t3, s)
    
    ex1.tStats = t_stats
    
def p_value():
    t_test()
    p_values = stats.t.sf(np.abs(ex1.tStats), ex1.sampleSize-1)*2
    ex1.pValues = p_values
    
def printtStats():
    t_test()
    dp.printmat(ex1.tStats, row_labels=["Zone1", "Zone2", "Zone3", "Zone4", "Whole Region"], col_labels=ex1.HHMeancolLabel)
    
def printpValues():
    p_value()
    dp.printmat(ex1.pValues, row_labels=["Zone1", "Zone2", "Zone3", "Zone4", "Whole Region"], col_labels=ex1.HHMeancolLabel)

