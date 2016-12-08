# import Ex_1 as ex1
# import Ex_2_1 as ex2_1
import TripGeneration.Production as pro
import TripGeneration.Attraction as attr
import TripDistribution.GravityModel

if __name__ == '__main__':
#     ex2_1.printCorrMatModel1()
#     ex2_1.printCorrMatModel2()
#     ex2_1.printCorrMatModel3()
    
#     ex2_1.printCoefficientModel3()
#     pro.PrintBusTripRecord()
#     pro.test()
#     pro.printCoefficientModel3()

#     pro.PrintCarTripRecord()
#     pro.printCorrMat("Bus", 3)
#     pro.printCoefficient("Car", 1)
#     pro.printCoefficient("Car", 2)
#     pro.printCoefficient("Car", 3)
#     pro.PrintCoefficient2("Car", 3)

#     oi = pro.oi("Car", 1, 0)
#     print oi

#     dj = attr.dj("Car", 1, 0)
#     print dj

#     attr.PrintBusAttraction()
#     attr.PrintCarAttraction()
#     attr.printCorrMat("Bus", 1)
    
#     pro.printCoefficient("Bus", 1)
    
#     attr.printCoefficient("Car", 1)

#     gm0 = TripDistribution.GravityModel.GravityModel("Bus", 1)
#     gm0.runGMBus(0.0001)
    
    gm1 = TripDistribution.GravityModel.GravityModel("Car", 1)
    gm1.runGMCar(0.0001)
    
    


