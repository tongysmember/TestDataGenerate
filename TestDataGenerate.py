#!/usr/bin/python

import csv
import os, os.path
import datetime
import string
import random
import re
from decimal import *

ExportPath     = './Generated/'
ExportFileName = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.csv'

global ExportContext
global ExportFileRows
global SpecDataRowTemplate
ExportFileRows = 1000


def ReadDDL2SpecData()->list:
    print('ReadSpec')
    global SpecDataRowTemplate

    SpecDataRowTemplate=['varchar(10)','varchar(20)','integer(30)', 'date', 'decimal(18,4)', 'decimal(38,4)']

def GenDatatable():
    print('GenDatatable')
    global ExportContext
    ExportContext = []
    for _ in range(ExportFileRows):
        ExportContext.append(SpecDataRowTemplate)

def GenDataContextBySpec():
    print('GenDataContextByDDL')
    global ExportContext
    ExportContext2 = []    

    for Row in ExportContext:
        Row = GenVarcharData(Row)
        Row = GenDateData(Row)
        Row = GenIntegerData(Row)
        Row = GenDecimalData(Row)
        ExportContext2.append(Row)

    ExportContext = ExportContext2

############################# Column Data Column Context Generate #############################
def GenByteintData(SrcRow)->list:
    print('GenByteintData')
    return []

def GenSmallintData(SrcRow)->list:
    print('GenSmallintData')
    return []

def GenBigintData(SrcRow)->list:
    print('GenBigintData')
    return []

def GenNumericData(SrcRow)->list:
    print('GenNumericData')
    return []

def GenFloatData(SrcRow)->list:
    print('GenFloatData')
    return []

def GenCharData(SrcRow)->list:
    print('GenCharData')
    return []

def GenTimeData(SrcRow)->list:
    print('GenTimeData')
    return []

def GenTimestampData(SrcRow)->list:
    print('GenTimestampData')
    return []

def GenVarcharData(SrcRow)->list:
    reg = re.compile(r'varchar\((\d+)')
    re_match = reg.findall(','.join(SrcRow))

    for Varlength in re_match:
        strRandomVarchar = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(int(Varlength)))
        SrcRow = [Row.replace('varchar('+Varlength+')', strRandomVarchar ) for Row in SrcRow]

    ConvertRow = SrcRow
    return ConvertRow 

def GenIntegerData(SrcRow)->list:
    reg = re.compile(r'integer\((\d+)')
    re_match = reg.findall(','.join(SrcRow))
    
    for Integerlength in re_match:
        SrcRow = [Row.replace('integer('+Integerlength+')', str(random.randint(0,int('9' * int(Integerlength))))) for Row in SrcRow]

    ConvertRow = SrcRow
    return ConvertRow 

def GenDateData(SrcRow)->list:
    ConvertRow =  list(map(lambda x: str.replace(x, "date", str(datetime.datetime.now().strftime("%Y%m%d"))), SrcRow))
    return ConvertRow 

def GenDecimalData(SrcRow)->list:
    reg = re.compile(r'decimal\((\d+\,\d+)')
    re_match = reg.findall(','.join(SrcRow))
    
    for Decimallength in re_match:
        IntLen, FloatLen = Decimallength.split(',')
        strRandomDecimal = str(random.randint(0,int('9' * int(IntLen))))
        strRandomDecimal = strRandomDecimal[:int(FloatLen)*-1]+'.'+strRandomDecimal[int(FloatLen)*-1:]
        SrcRow = [Row.replace('decimal('+Decimallength+')', strRandomDecimal) for Row in SrcRow]

    ConvertRow = SrcRow
    return ConvertRow 

############################# Column Data Column Context Generate #############################

def ExportFile():
    print('ExportFile')
    global ExportContext
    os.makedirs(os.path.dirname(ExportPath), exist_ok=True)
    with open( ExportPath + ExportFileName, 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(ExportContext)

if __name__=='__main__':

    #讀取DDL欄位資訊
    ReadDDL2SpecData()

    #產生空List待填資料
    GenDatatable()

    #依據欄位資訊產生隨機資料
    GenDataContextBySpec()

    #輸出檔案
    ExportFile()

