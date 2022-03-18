#!/usr/bin/python

import csv
import os, os.path
import datetime
import string
import random
import re
from decimal import *

from collections import Iterable


ExportPath     = './Generated/'
DDLPath     = './DDL/Teradata.DDL'
ExportFileName = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.csv'

global ExportContext
global ExportFileRows
global SpecDataRowTemplate
global SpecHeaderRowTemplate
global SpecExportRowTemplate
ExportFileRows = 10

def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item


def ReadDDL2SpecData()->list:
    print('ReadSpec')
    global SpecDataRowTemplate
    global SpecHeaderRowTemplate
    global SpecExportRowTemplate
    #SpecDataRowTemplate=['varchar(10)','varchar(20)','integer(30)', 'date', 'decimal(18,4)', 'decimal(38,4)']
    DDLcontents = None
    with open(DDLPath) as f:
        DDLcontents = f.read().upper()
        #print(DDLcontents)
    
    SpecHeaderRowTemplate, SpecDataRowTemplate = DDLcontextRegex(DDLcontents)
    
    SpecExportRowTemplate =  []
    for row in SpecDataRowTemplate:
        if (row[1] != ''):
            SpecExportRowTemplate.append(row[0]+'('+row[1]+')')
        else:
            SpecExportRowTemplate.append(row[0])
    
        


def DDLcontextRegex(SrcDDLcontents)->list:
    re_script = r"""\s* (?P<column_name>\w+)\s+ (?P<column_type>\w+) (?:     \(     (?P<column_size>[^()]+)     \) )? [,) ]+ .*"""
    DataTypeList = ['BYTEINT',
                    'SMALLINT',
                    'INTEGER',
                    'BIGINT',
                    'DECIMAL',
                    'NUMERIC',
                    'FLOAT',
                    'CHAR',
                    'VARCHAR',
                    'DATE',
                    'TIME',
                    'TIMESTAMP']
    # DataTypeList Upper Type
    reg = re.compile(re_script, re.VERBOSE | re.IGNORECASE)

    re_match = reg.findall(SrcDDLcontents)
    DDL_Context =[]
    DDL_Header =[]
    for ColName, ColType, ColLength in re_match:
        if ColType in DataTypeList:
            #print('{0},{1},{2}'.format(ColName, ColType, ColLength))
            DDL_Context.append([ColType, ColLength])
            DDL_Header.append([ColName])
    
    return DDL_Header,DDL_Context


def GenDatatable():
    print('GenDatatable')
    global ExportContext
    ExportContext = []
    for _ in range(ExportFileRows):
        ExportContext.append(SpecDataRowTemplate)

def GenDataContextBySpec():
    print('GenDataContextByDDL')
    global ExportContext
    global SpecExportRowTemplate
    global SpecExportRowTemplate
    SpecExportRowRandom = SpecExportRowTemplate
    ExportContextGenData = []    
    for _ in range(ExportFileRows):
        for Row in SpecExportRowTemplate:
            if 'VARCHAR' in Row:
                SpecExportRowRandom = GenVarcharData(SpecExportRowRandom) 
            if 'DATE' in Row:
                SpecExportRowRandom = GenDateData(SpecExportRowRandom)
            if 'INTEGER' in Row:
                SpecExportRowRandom = GenIntegerData(SpecExportRowRandom)
            if 'DECIMAL' in Row:
                SpecExportRowRandom = GenDecimalData(SpecExportRowRandom)
            if 'TIMESTAMP' in Row:
                SpecExportRowRandom = GenTimestampData(SpecExportRowRandom)
        ExportContextGenData.append(SpecExportRowRandom)
        SpecExportRowRandom = SpecExportRowTemplate
    
    #ExportContextGenData.append(SpecExportRowTemplate)

    ExportContext = ExportContextGenData

############################# Column Data Column Context Generate #############################

def GenByteintData(SrcRow)->list:
    print('GenByteintData')
    return []

def GenSmallintData(SrcRow)->list:
    print('GenSmallintData')
    return []

def GenIntegerData(SrcRow)->list:
    reg = re.compile(r'INTEGER\((\d+)')
    re_match = reg.findall(','.join(SrcRow))
    
    for Integerlength in re_match:
        SrcRow = [Row.replace('integer('+Integerlength+')', str(random.randint(0,int('9' * int(Integerlength))))) for Row in SrcRow]

    ConvertRow = SrcRow
    return ConvertRow 

def GenBigintData(SrcRow)->list:
    print('GenBigintData')
    return []

def GenDecimalData(SrcRow)->list:
    reg = re.compile(r'DECIMAL\((\d+\,\d+)')
    re_match = reg.findall(','.join(SrcRow))
    
    for Decimallength in re_match:
        IntLen, FloatLen = Decimallength.split(',')
        strRandomDecimal = str(random.randint(0,int('9' * int(IntLen))))
        strRandomDecimal = strRandomDecimal[:int(FloatLen)*-1]+'.'+strRandomDecimal[int(FloatLen)*-1:]
        SrcRow = [Row.replace('decimal('+Decimallength+')', strRandomDecimal) for Row in SrcRow]

    ConvertRow = SrcRow
    return ConvertRow 

def GenNumericData(SrcRow)->list:
    print('GenNumericData')
    return []

def GenFloatData(SrcRow)->list:
    print('GenFloatData')
    return []

def GenCharData(SrcRow)->list:
    print('GenCharData')
    return []

def GenVarcharData(SrcRow)->list:
    #SrcRow = list(flatten(SrcRow))
    reg = re.compile(r'VARCHAR\((\d+)')
    re_match = reg.findall(','.join(list(flatten(SrcRow))))
    #re_match = reg.findall(SrcRow)

    for Varlength in re_match:
        strRandomVarchar = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(int(Varlength)))
        SrcRow = [Row.replace('VARCHAR('+Varlength+')', strRandomVarchar ) for Row in SrcRow]

    ConvertRow = SrcRow
    return ConvertRow   

def GenDateData(SrcRow)->list:
    #"%H%M%S"
    ConvertRow =  list(map(lambda x: str.replace(x, "DATE", str((datetime.datetime.now()+ datetime.timedelta(days=int(random.choice(string.digits)))).strftime("%Y%m%d"))), SrcRow))

    return ConvertRow   

def GenTimeData(SrcRow)->list:
    #HHMMSS.nnnnnn
    ConvertRow =  list(map(lambda x: str.replace(x, "TIME", str((datetime.datetime.now()+ datetime.timedelta(days=int(random.choice(string.digits)))).strftime("%H%M%S")+'.'+random.choice(string.digits)*6)), SrcRow))

    return ConvertRow

def GenTimestampData(SrcRow)->list:
    #YYMMDDHHMMSS.nnnnnn
    ConvertRow =  list(map(lambda x: str.replace(x, "TIMESTAMP", str((datetime.datetime.now()+ datetime.timedelta(days=int(random.choice(string.digits)))).strftime("%Y%m%d%H%M%S")+'.'+random.choice(string.digits)*6)), SrcRow))
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

