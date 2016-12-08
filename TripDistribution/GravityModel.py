import numpy as np
import excel as ex
import display as dp
import TripGeneration.Attraction as attr
import TripGeneration.Production as prod

filename = "CEE220A_Survey_Data.xlsx"

class GravityModel():
    def __init__(self, alt, time):
#         np.set_printoptions(precision=5, suppress=True)
        self.tijBus = self.opensheet("SurveyOD Bus")
        self.tijCar = self.opensheet("SurveyOD Car")
        
        self.oi = prod.oi(alt, 1, time)
        self.dj = attr.dj(alt, 1, time)
        
        self.adjOi = self.oi
        self.adjDj = self.adjDjF(self.oi, self.dj)
        
        print self.oi
        print self.dj
        print self.adjDj
        
        self.cijBus = self.opensheet("Forecast Zonal Travel Times Bus")
        
        self.cijCar = self.opensheet("Forecast Zonal Travel Times Car")
        
    def opensheet(self, sheetname):
        cijArr = ex.excelToArray(filename, sheetname)
        cij = cijArr[:, 1:]
        return cij
        
        
    def adjDjF(self, oi, dj):
        sumOi = np.sum(oi)
        sumDj = np.sum(dj)
        
        diffSum = sumOi - sumDj
        
        adjVal = np.multiply(float(diffSum) / float(sumDj), dj)
        
        adjDj = np.round(dj + adjVal, 0)
        
        if sumOi != np.sum(adjDj):
            diff = sumOi - np.sum(adjDj)
            adjDj[0]+=diff
        
        return adjDj
    

        
        

    def calcBar(self, tij, cij):
        tijcij = float(np.sum(np.multiply(tij, cij)))
        sumtij = float(np.sum(tij))
        
        cBar = tijcij / sumtij
        return cBar
        
    def iterationAB(self, tij, oi, dj, cij, mu, threshold):
        tij = tij
        cij = cij
                
        aList = []
        bList = []    
        diff = 999
        iterInd = 0 #
        ai = np.ones((len(oi),1))
        bj = np.zeros((len(dj),1))
        aList.append(ai)
        
        
    #     ai = np.atleast_2d(np.asarray(ai)).T
    #     bj = np.atleast_2d(np.asarray(bj)).T
         
        while diff > threshold:
            bj=np.zeros((len(bj),1))
            ind = 0
            while ind < len(cij):
                e_mucij = np.atleast_2d(np.exp(-mu*cij[:, ind])).T
                aoe_mucij1 = np.multiply(ai, oi)
                aoe_mucij2 = np.multiply(aoe_mucij1, e_mucij)
                b_1 = np.sum(aoe_mucij2)
                b= b_1**-1
                bj[ind][0]=b
                ind+=1
            bList.append(bj)
            
            ai=np.zeros((len(bj),1))
            ind = 0
            while ind < len(cij):
                e_mucij = np.atleast_2d(np.exp(-mu*cij[ind, :])).T
                aoe_mucij1 = np.multiply(bj, dj)
                aoe_mucij2 = np.multiply(aoe_mucij1, e_mucij)
                a_1 = np.sum(aoe_mucij2)
                a= a_1**-1
        
                ai[ind][0]=a
                ind+=1
            aList.append(ai)
            
            diff = float(abs(aList[-1][0]-aList[-2][0]))
            
            
            if diff < threshold:
                break
            else:
                iterInd +=1
        
        return (aList, bList)
    
    def tijHat(self, ai, bj, oi, dj, mu, cij):
        i = 0
        j = 0
        
        tijHat = np.zeros((len(ai), len(bj)))
         
        while i < len(ai):
            j = 0
            while j < len(bj):
                tijHat[i][j]=ai[i]*bj[j]*oi[i]*dj[j]*np.exp(-mu*cij[i][j])
                j+=1
            i+=1
        
        return tijHat
    
    
    def runGMBus(self, threshold):
        ind = 0
        tij = self.tijBus
        cij = self.cijBus
        oi = self.adjOi
        dj = self.adjDj
        
        cBar1 = 0
        cBar2 = self.calcBar(tij, cij)
        mu1 = 0
        mu2 = cBar2**-1
        
        diff = 999
        
        while threshold < diff:
            abList = self.iterationAB(tij, oi, dj, cij, mu2, 0.0001)
            
            a = abList[0]
            a2 = []
            for i in a:
                i = i.tolist()
                flati = [val for sublist in i for val in sublist]
                a2.append(flati)
            
            b = abList[1]
            b2 = []
            for i in b:
                i = i.tolist()
                flati = [val for sublist in i for val in sublist]
                b2.append(flati)
            dp.printmat(a2)
            dp.printmat(b2)
            
             
            aList = abList[0][-1]
            bList = abList[1][-1]
            
            tij = self.tijHat(aList, bList, oi, dj, mu2, cij)
            cBar1 = cBar2
            cBar2 = self.calcBar(tij, cij)
            
            mu1 = mu2
            mu2 = cBar2/cBar1*mu1
        
            diff = float(abs(mu1-mu2))
            
            ind+=1
            
            print "#Iteration: ", "%d" % ind
            print "mu: ", "%.3f" % mu1

            dp.printmat(tij, row_labels=['Zone1', 'Zone2', 'Zone3', 'Zone4'], col_labels=['Zone1', 'Zone2', 'Zone3', 'Zone4'])
            
    def runGMCar(self, threshold):
        ind = 0
        tij = self.tijCar
        cij = self.cijCar
        oi = self.adjOi
        dj = self.adjDj
        
        cBar1 = 0
        cBar2 = self.calcBar(tij, cij)
        mu1 = 0
        mu2 = cBar2**-1
        
        diff = 999
        
        while threshold < diff:
            abList = self.iterationAB(tij, oi, dj, cij, mu2, 0.0001)
            
            a = abList[0]
            a2 = []
            for i in a:
                i = i.tolist()
                flati = [val for sublist in i for val in sublist]
                a2.append(flati)
            
            b = abList[1]
            b2 = []
            for i in b:
                i = i.tolist()
                flati = [val for sublist in i for val in sublist]
                b2.append(flati)
            dp.printmat(a2)
            dp.printmat(b2)
            
             
            aList = abList[0][-1]
            bList = abList[1][-1]
            
            tij = self.tijHat(aList, bList, oi, dj, mu2, cij)
            cBar1 = cBar2
            cBar2 = self.calcBar(tij, cij)
            
            mu1 = mu2
            mu2 = cBar2/cBar1*mu1
        
            diff = float(abs(mu1-mu2))
            
            ind+=1
            
            print "#Iteration: ", "%d" % ind
            print "mu: ", "%.3f" % mu1

            dp.printmat(tij, row_labels=['Zone1', 'Zone2', 'Zone3', 'Zone4'], col_labels=['Zone1', 'Zone2', 'Zone3', 'Zone4'])
            