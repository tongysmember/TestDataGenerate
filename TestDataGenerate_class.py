#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import os, os.path
import datetime
import re
from decimal import *

import GenDataType


ExportPath     = './Generated/'
DDLPath     = './DDL/Teradata.DDL'
ExportFileName = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.csv'

global ExportContext
global ExportFileRows
global SpecDataRowTemplate
global SpecHeaderRowTemplate
global SpecExportRowTemplate
ExportFileRows = 10

def ReadDDL2SpecData()->list:
    print('ReadSpec')
    global SpecDataRowTemplate
    global SpecHeaderRowTemplate
    global SpecExportRowTemplate

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

    #GenDataObj = GenDataType()

    for _ in range(ExportFileRows):
        for Row in SpecExportRowTemplate:
            if 'VARCHAR' in Row:
                #SpecExportRowRandom = GenVarcharData(SpecExportRowRandom) 
                SpecExportRowRandom = GenDataType.GenByteintData(SpecExportRowRandom)
            if 'CHAR' in Row:
                SpecExportRowRandom = GenDataType.GenCharData(SpecExportRowRandom) 
            if 'DATE' in Row:
                SpecExportRowRandom = GenDataType.GenDateData(SpecExportRowRandom)
            if 'INTEGER' in Row:
                SpecExportRowRandom = GenDataType.GenIntegerData(SpecExportRowRandom)
            if 'SMALLINT' in Row:
                SpecExportRowRandom = GenDataType.GenSmallintData(SpecExportRowRandom)
            if 'BIGINT' in Row:
                SpecExportRowRandom = GenDataType.GenBigintData(SpecExportRowRandom)
            if 'DECIMAL' in Row:
                SpecExportRowRandom = GenDataType.GenDecimalData(SpecExportRowRandom)
            if 'NUMERIC' in Row:
                SpecExportRowRandom = GenDataType.GenNumericData(SpecExportRowRandom)
            if 'FLOAT' in Row:
                SpecExportRowRandom = GenDataType.GenFloatData(SpecExportRowRandom)
            if 'TIMESTAMP' in Row:
                SpecExportRowRandom = GenDataType.GenTimestampData(SpecExportRowRandom)
            if 'TIME' in Row:
                SpecExportRowRandom = GenDataType.GenTimeData(SpecExportRowRandom)
            if 'BYTEINT' in Row:
                SpecExportRowRandom = GenDataType.GenByteintData(SpecExportRowRandom)

        ExportContextGenData.append(SpecExportRowRandom)
        SpecExportRowRandom = SpecExportRowTemplate
    
    #ExportContextGenData.append(SpecExportRowTemplate)

    ExportContext = ExportContextGenData

def ExportFile():
    print('ExportFile')
    global ExportContext
    global SpecHeaderRowTemplate
    global BoolExportHeaderRow
    global BoolExportCountRow

    HeaderRow = [(list(GenDataType.flatten(SpecHeaderRowTemplate)))]

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

