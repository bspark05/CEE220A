#-*- coding: utf-8 -*-

import xlrd
import numpy as np
import openpyxl

def excelRead(filepath, sheetname):
    workbook = xlrd.open_workbook(filepath)
    worksheet = workbook.sheet_by_name(sheetname)
    
    num_rows = worksheet.nrows -1
    curr_row = -1
    result = []
    
    while curr_row < num_rows:
        curr_row += 1
        row = worksheet.row(curr_row)
        result.append(row)
    
    return result


def excelToArray(filepath, sheetname):
    varExcel = excelRead(filepath, sheetname)
    varList = []
    # first row is a field name
    for row in varExcel[1:]:
        rowList = []
        for value in row:
            rowList.append(float(value.value))
        varList.append(rowList)
    varArray = np.array(varList)
    # transpose the array
#     varArrayTras = np.transpose(varArray)
    
    return varArray

def excelWriteOnExistingFile(filepath, sheetname, columnNum, insert, woFirst=1): 
    wb = xlrd.open_workbook(filepath)
    ws = wb.sheet_by_name(sheetname)
    
    workbook = openpyxl.load_workbook(filepath)
    worksheet = workbook.active
    
    end_rows = ws.nrows
    curr_row = 0
    insert_rows = len(insert) 
    colInd = len(insert[0])
        
    colNum = columnNum    
    asciiNum = ord(colNum)
    
    indx = 0
    colDigit=0
    
    while indx < colInd:
        curr_row=0
        while curr_row < insert_rows-woFirst:
            curr_row += 1

            try:
                worksheet[colNum+str(end_rows+curr_row)] = insert[curr_row-1+woFirst][indx]
            except(TypeError):
                print('Type Error - '+str(indx))
                
        
        asciiNum += 1
        if asciiNum > 90:
            colDigit+=1
            asciiNum -= 26
        if colDigit == 0:
            colNum=chr(asciiNum)
        else:
            colNum=chr(colDigit+64)+chr(asciiNum)
            
            
        indx+=1     
            
                 
    workbook.save(filepath)
    print('saved successfully in existing file!')


