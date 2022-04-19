#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import os, os.path
import datetime
import re
from decimal import *

import GenDataType
from DataTypeEnum import DataType
import logging
import os.path

ExportPath   = './Generated/'
LogPath      = './Log/'

global ExportContext
global ExportFileRows
global SpecDataRowTemplate
global SpecHeaderRowTemplate
global SpecExportRowTemplate

def ReadDDL2SpecData()->list:
    ''' Read DDL File and Generate Column Data '''

    #print('ReadSpec')
    global SpecDataRowTemplate
    global SpecHeaderRowTemplate
    global SpecExportRowTemplate

    DDLcontents = None
    #with open(sys.argv[4]) as f:
    with open(GenDataType.CheckSecurityInput(sys.argv[4])) as f:
        DDLcontents = f.read().upper() #正規化
    
    SpecHeaderRowTemplate, SpecDataRowTemplate = DDLcontextRegex(DDLcontents)
    
    SpecExportRowTemplate =  []
    for Col in SpecDataRowTemplate:
        if (Col[1] != ''):
            SpecExportRowTemplate.append(Col[0]+'('+Col[1]+')')
        else:
            SpecExportRowTemplate.append(Col[0])
    
def DDLcontextRegex(SrcDDLcontents)->list:
    ''' Regex DDL to Extract Column Data, Create Header & Context '''

    re_script = r"""\s* (?P<column_name>\w+)\s+ (?P<column_type>\w+) (?:     \(     (?P<column_size>[^()]+)     \) )? [, \n ) ] """
    DataTypeList = [EnumRow.name for EnumRow in DataType]
    # DataTypeList Upper Type
    reg = re.compile(re_script, re.VERBOSE | re.IGNORECASE)

    re_match = reg.findall(SrcDDLcontents)
    DDL_Context =[]
    DDL_Header =[]
    for ColName, ColType, ColLength in re_match:
        if ColType in DataTypeList:
            DDL_Context.append(['^'+ColType+'$', ColLength])
            DDL_Header.append([ColName])
    
    return DDL_Header,DDL_Context

def GenDataContextBySpec():
    ''' Generated Row Data By Column Context '''

    global ExportContext
    global SpecExportRowTemplate
    SpecExportRowTemplate = [col.replace(' ','') for col in SpecExportRowTemplate] ## 去除空白字串
    SpecExportRowRandom = SpecExportRowTemplate
    ExportContextGenData = []    
    
    for _ in range(ExportFileRows):
        for Col in SpecExportRowTemplate:
            SpecExportRowRandom = GenDataType.GenDataType(Col.split('$')[0].replace('^',''),SpecExportRowRandom)

        ExportContextGenData.append(SpecExportRowRandom)
        SpecExportRowRandom = SpecExportRowTemplate
    
    #ExportContextGenData.append(SpecExportRowTemplate)

    ExportContext = ExportContextGenData

def ExportFile():
    ''' Create CSV Data File to Spec Path '''

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
    ''' Checking Argv Parameter '''
    
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
    ''' Set Loggin Format '''

    FileName, FileFormat = datetime.datetime.now().strftime("%Y%m%d"),'.log'
    logging.basicConfig(filename=LogPath+FileName+FileFormat,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)    

if __name__=='__main__':
    try:
        
        LoggingSetting()

        #執行程式相關設定
        ExportFileSetting()

        #讀取DDL欄位資訊
        ReadDDL2SpecData()

        #依據欄位資訊產生隨機資料
        GenDataContextBySpec()

        #輸出檔案
        ExportFile()

    except Exception as e:
        print(e)
        logging.error(e)