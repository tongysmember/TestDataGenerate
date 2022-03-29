#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import os, os.path
import datetime
import re
from decimal import *

import GenDataType
import logging
import os.path

ExportPath   = './Generated/'
LogPath      = './Log/'
#DDLPath     = './DDL/Teradata.DDL'
#DDLPath     = './DDL/ACPBCOSMT.txt'
#DDLPath     = './DDL/ACPBCOSQT.txt'
#DDLPath     = './DDL/ACPBCOSYT.txt'
#ExportFileName = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.csv'

global ExportContext
global ExportFileRows
global SpecDataRowTemplate
global SpecHeaderRowTemplate
global SpecExportRowTemplate

def ReadDDL2SpecData()->list:
    #print('ReadSpec')
    global SpecDataRowTemplate
    global SpecHeaderRowTemplate
    global SpecExportRowTemplate

    DDLcontents = None
    with open(sys.argv[4]) as f:
        DDLcontents = f.read().upper() #正規化
    
    SpecHeaderRowTemplate, SpecDataRowTemplate = DDLcontextRegex(DDLcontents)
    
    SpecExportRowTemplate =  []
    for row in SpecDataRowTemplate:
        if (row[1] != ''):
            SpecExportRowTemplate.append(row[0]+'('+row[1]+')')
        else:
            SpecExportRowTemplate.append(row[0])
    
def DDLcontextRegex(SrcDDLcontents)->list:
    re_script = r"""\s* (?P<column_name>\w+)\s+ (?P<column_type>\w+) (?:     \(     (?P<column_size>[^()]+)     \) )? [, \n ) ] """
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
    #print('GenDatatable')
    global ExportContext
    ExportContext = []
    for _ in range(ExportFileRows):
        ExportContext.append(SpecDataRowTemplate)

def GenDataContextBySpec():
    #print('GenDataContextByDDL')
    global ExportContext
    global SpecExportRowTemplate
    SpecExportRowTemplate = [col.replace(' ','') for col in SpecExportRowTemplate] ## 去除空白字串
    SpecExportRowRandom = SpecExportRowTemplate
    ExportContextGenData = []    

    #GenDataObj = GenDataType()

    for _ in range(ExportFileRows):
        for Col in SpecExportRowTemplate:
            if 'VARCHAR' in Col:
                #SpecExportRowRandom = GenVarcharData(SpecExportRowRandom) 
                SpecExportRowRandom = GenDataType.GenVarcharData(SpecExportRowRandom)
            if 'CHAR' in Col:
                SpecExportRowRandom = GenDataType.GenCharData(SpecExportRowRandom) 
            if 'DATE' in Col:
                SpecExportRowRandom = GenDataType.GenDateData(SpecExportRowRandom)
            if 'INTEGER' in Col:
                SpecExportRowRandom = GenDataType.GenIntegerData(SpecExportRowRandom)
            if 'SMALLINT' in Col:
                SpecExportRowRandom = GenDataType.GenSmallintData(SpecExportRowRandom)
            if 'BIGINT' in Col:
                SpecExportRowRandom = GenDataType.GenBigintData(SpecExportRowRandom)
            if 'DECIMAL' in Col:
                SpecExportRowRandom = GenDataType.GenDecimalData(SpecExportRowRandom)
            if 'NUMERIC' in Col:
                SpecExportRowRandom = GenDataType.GenNumericData(SpecExportRowRandom)
            if 'FLOAT' in Col:
                SpecExportRowRandom = GenDataType.GenFloatData(SpecExportRowRandom)
            if 'TIMESTAMP' in Col:
                SpecExportRowRandom = GenDataType.GenTimestampData(SpecExportRowRandom)
            if 'TIME' in Col:
                SpecExportRowRandom = GenDataType.GenTimeData(SpecExportRowRandom)
            if 'BYTEINT' in Col:
                SpecExportRowRandom = GenDataType.GenByteintData(SpecExportRowRandom)

        ExportContextGenData.append(SpecExportRowRandom)
        SpecExportRowRandom = SpecExportRowTemplate
    
    #ExportContextGenData.append(SpecExportRowTemplate)

    ExportContext = ExportContextGenData

def ExportFile():
    print('輸出資料中')
    global ExportContext
    global SpecHeaderRowTemplate
    global BoolExportHeaderRow
    global BoolExportCountRow

    HeaderRow = [(list(GenDataType.flatten(SpecHeaderRowTemplate)))]
    ExportFileName = os.path.splitext(sys.argv[4])[0].split('/')[-1] +'_'+ datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.csv'

    os.makedirs(os.path.dirname(ExportPath), exist_ok=True)
    with open( ExportPath + ExportFileName, 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if BoolExportHeaderRow : writer.writerows(HeaderRow)
        writer.writerows(ExportContext)
        if BoolExportCountRow : writer.writerows([['****'+str(ExportFileRows)]])
    print('輸出檔案 : '+ExportPath + ExportFileName)

def ExportFileSetting():
    try:
        global BoolExportHeaderRow
        global BoolExportCountRow 
        global ExportFileRows

        if len(sys.argv) != 5:
            print('請輸入相關設定, 尚未完整輸入')
            logging.error('argv-Error============')
            logging.error(list(sys.argv)[1:])
            sys.exit()   

        BoolExportHeaderRow = 1 if sys.argv[1].upper() == 'Y' else 0 
        BoolExportCountRow = 1 if sys.argv[2].upper() == 'Y' else 0 
        
        if int(sys.argv[3]) > 0:
            ExportFileRows = int(sys.argv[3])
        else:
            print('請輸入正確正整數')
            logging.error('請輸入正確正整數 : '+sys.argv[3])
            sys.exit()
        
        if not(os.path.exists(sys.argv[4])):
            print('請輸入正確DDL路徑')
            logging.error('請輸入正確DDL路徑 : '+sys.argv[4])
            sys.exit()

    except Exception as e:
        print('輸入資料錯誤')
        logging.error(e)
        sys.exit()

def LoggingSetting():
    FileName, FileFormat = datetime.datetime.now().strftime("%Y%m%d"),'.log'
    logging.basicConfig(filename=LogPath+FileName+FileFormat,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)    

if __name__=='__main__':
    
    LoggingSetting()

    #執行程式相關設定
    ExportFileSetting()

    #讀取DDL欄位資訊
    ReadDDL2SpecData()

    #依據欄位資訊產生隨機資料
    GenDataContextBySpec()

    #輸出檔案
    ExportFile()

