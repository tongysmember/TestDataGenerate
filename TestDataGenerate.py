#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
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
        DDLcontents = f.read().upper() #正規化
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
            if 'CHAR' in Row:
                SpecExportRowRandom = GenCharData(SpecExportRowRandom) 
            if 'DATE' in Row:
                SpecExportRowRandom = GenDateData(SpecExportRowRandom)
            if 'INTEGER' in Row:
                SpecExportRowRandom = GenIntegerData(SpecExportRowRandom)
            if 'SMALLINT' in Row:
                SpecExportRowRandom = GenSmallintData(SpecExportRowRandom)
            if 'BIGINT' in Row:
                SpecExportRowRandom = GenBigintData(SpecExportRowRandom)
            if 'DECIMAL' in Row:
                SpecExportRowRandom = GenDecimalData(SpecExportRowRandom)
            if 'NUMERIC' in Row:
                SpecExportRowRandom = GenNumericData(SpecExportRowRandom)
            if 'FLOAT' in Row:
                SpecExportRowRandom = GenFloatData(SpecExportRowRandom)
            if 'TIMESTAMP' in Row:
                SpecExportRowRandom = GenTimestampData(SpecExportRowRandom)
            if 'TIME' in Row:
                SpecExportRowRandom = GenTimeData(SpecExportRowRandom)
            if 'BYTEINT' in Row:
                SpecExportRowRandom = GenByteintData(SpecExportRowRandom)
        ExportContextGenData.append(SpecExportRowRandom)
        SpecExportRowRandom = SpecExportRowTemplate
    
    #ExportContextGenData.append(SpecExportRowTemplate)

    ExportContext = ExportContextGenData

############################# Column Data Column Context Generate #############################

def GenByteintData(SrcRow)->list:
    #-128 to +127
    return [Row.replace('BYTEINT', str(random.randint(-128, +127))) for Row in SrcRow] 

def GenSmallintData(SrcRow)->list:
    #-32768 ~ +32767
    return [Row.replace('SMALLINT', str(random.randint(-32768 , +32767))) for Row in SrcRow] 

def GenIntegerData(SrcRow)->list:
    #-2,147,483,648 ~ +2,147,483,647
    return [Row.replace('INTEGER', str(random.randint(-2147483648, 2147483647))) for Row in SrcRow] 

def GenBigintData(SrcRow)->list:
    #-9,233,372,036,854,775,808 to +9,233,372,036,854,775,807
    return [Row.replace('BIGINT', str(random.randint(-9233372036854775808 , +9233372036854775807))) for Row in SrcRow] 

def GenDecimalData(SrcRow)->list:
    reg = re.compile(r'DECIMAL\((\d+\,\d+)')
    re_match = reg.findall(','.join(SrcRow))
    
    for Decimallength in re_match:
        IntLen, FloatLen = Decimallength.split(',')
        strRandomDecimal = str(random.randint(0,int('9' * int(IntLen))))
        strRandomDecimal = strRandomDecimal[:int(FloatLen)*-1]+'.'+strRandomDecimal[int(FloatLen)*-1:]
        SrcRow = [Row.replace('DECIMAL('+Decimallength+')', strRandomDecimal) for Row in SrcRow]

    ConvertRow = SrcRow
    return ConvertRow 

def GenNumericData(SrcRow)->list:
    reg = re.compile(r'NUMERIC\((\d+\,\d+)')
    re_match = reg.findall(','.join(SrcRow))
    
    for Decimallength in re_match:
        IntLen, FloatLen = Decimallength.split(',')
        strRandomDecimal = str(random.randint(0,int('9' * int(IntLen))))
        strRandomDecimal = strRandomDecimal[:int(FloatLen)*-1]+'.'+strRandomDecimal[int(FloatLen)*-1:]
        SrcRow = [Row.replace('NUMERIC('+Decimallength+')', strRandomDecimal) for Row in SrcRow]

    ConvertRow = SrcRow
    return ConvertRow 

def GenFloatData(SrcRow)->list:
    # Teradata : https://docs.teradata.com/r/WurHmDcDf31smikPbo9Mcw/RhAF_5yskR0MQJyrFVcSxQ
    # Represent values in sign/magnitude form ranging from 2.226 x 10-308 to 1.797 x 10308.

    return [Row.replace('FLOAT', str(random.uniform(-999.999, +999.999))) for Row in SrcRow] 

def GenCharData(SrcRow)->list:
    #SrcRow = list(flatten(SrcRow))
    reg = re.compile(r'CHAR\((\d+)')
    re_match = reg.findall(','.join(list(flatten(SrcRow))))
    #re_match = reg.findall(SrcRow)

    for Varlength in re_match:
        strRandomVarchar = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(int(Varlength)))
        SrcRow = [Row.replace('CHAR('+Varlength+')', strRandomVarchar ) for Row in SrcRow]

    ConvertRow = SrcRow
    return ConvertRow   

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
    return list(map(lambda x: str.replace(x, "DATE", str((datetime.datetime.now()+ datetime.timedelta(days=int(random.choice(string.digits)))).strftime("%Y%m%d"))), SrcRow))
   
def GenTimeData(SrcRow)->list:
    #HHMMSS.nnnnnn
    return list(map(lambda x: str.replace(x, "TIME", str((datetime.datetime.now()+ datetime.timedelta(days=int(random.choice(string.digits)))).strftime("%H%M%S")+'.'+random.choice(string.digits)*6)), SrcRow))

def GenTimestampData(SrcRow)->list:
    #YYMMDDHHMMSS.nnnnnn
    return list(map(lambda x: str.replace(x, "TIMESTAMP", str((datetime.datetime.now()+ datetime.timedelta(days=int(random.choice(string.digits)))).strftime("%Y%m%d%H%M%S")+'.'+random.choice(string.digits)*6)), SrcRow))


############################# Column Data Column Context Generate #############################

def ExportFile():
    print('ExportFile')
    global ExportContext
    global SpecHeaderRowTemplate
    global BoolExportHeaderRow
    global BoolExportCountRow

    HeaderRow = [(list(flatten(SpecHeaderRowTemplate)))]

    os.makedirs(os.path.dirname(ExportPath), exist_ok=True)
    with open( ExportPath + ExportFileName, 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if BoolExportHeaderRow : writer.writerows(HeaderRow)
        writer.writerows(ExportContext)
        if BoolExportCountRow : writer.writerows([['----------------------------'+str(ExportFileRows)]])

def ExportFileSetting():
    global BoolExportHeaderRow
    global BoolExportCountRow 

    if len(sys.argv) < 2:
        print('請輸入相關設定')
        sys.exit()   

    BoolExportHeaderRow = 1 if sys.argv[1].upper() == 'Y' else 0 
    BoolExportCountRow = 1 if sys.argv[2].upper() == 'Y' else 0 

if __name__=='__main__':

    #執行程式相關設定
    ExportFileSetting()

    #讀取DDL欄位資訊
    ReadDDL2SpecData()

    #產生空List待填資料
    GenDatatable()

    #依據欄位資訊產生隨機資料
    GenDataContextBySpec()

    #輸出檔案
    ExportFile()

