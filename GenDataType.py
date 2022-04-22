#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import datetime
import string
import random
import secrets
import sys

from collections.abc import Iterable
import re
from DataTypeEnum import DataType

def GenDataType(SrcDataType,SrcRow):
    ''' Choice Random Data Method by DataType '''

    if  'VARCHAR' == DataType[SrcDataType].name:
        return GenVarcharData(SrcRow)
    elif 'CHAR' == DataType[SrcDataType].name:
        return GenCharData(SrcRow) 
    elif 'DATE' == DataType[SrcDataType].name:
        return GenDateData(SrcRow)
    elif 'INTEGER' == DataType[SrcDataType].name:
        return GenIntegerData(SrcRow)
    elif 'SMALLINT' == DataType[SrcDataType].name:
        return GenSmallintData(SrcRow)
    elif 'BIGINT' == DataType[SrcDataType].name:
        return GenBigintData(SrcRow)
    elif 'DECIMAL' == DataType[SrcDataType].name:
        return GenDecimalData(SrcRow)
    elif 'NUMERIC' == DataType[SrcDataType].name:
        return GenNumericData(SrcRow)
    elif 'FLOAT' == DataType[SrcDataType].name:
        return GenFloatData(SrcRow)
    elif 'TIMESTAMP' == DataType[SrcDataType].name:
        return GenTimestampData(SrcRow)
    elif 'TIME' == DataType[SrcDataType].name:
        return GenTimeData(SrcRow)
    elif 'BYTEINT' == DataType[SrcDataType].name:
        return GenByteintData(SrcRow)     

def GenSecretRamdonDigitData(start:int, end:int)->str:
    ''' 產生加密亂數(數值), 輸入初始值與結束值範圍 '''
    return str(secrets.SystemRandom().randrange(start, end, 1))

def GenSecretRamdonTextData(length:int)->str:
    ''' 產生加密亂數(文字), 輸入產生文字長度 '''
    rndList = list(string.ascii_uppercase+string.digits)
    return "".join(secrets.SystemRandom().sample(rndList,length))

def GenByteintData(SrcRow)->list:
    #-128 to +127
    return [Row.replace('^BYTEINT$', GenSecretRamdonDigitData(0, 127), 1) for Row in SrcRow] 

def GenSmallintData(SrcRow)->list:
    #-32768 ~ +32767
    return [Row.replace('^SMALLINT$', GenSecretRamdonDigitData(0, +32767), 1) for Row in SrcRow] 


def GenIntegerData(SrcRow)->list:
    #-2,147,483,648 ~ +2,147,483,647
    return [Row.replace('^INTEGER$', GenSecretRamdonDigitData(0, +2147483647), 1) for Row in SrcRow] 


def GenBigintData(SrcRow)->list:
    #-9,233,372,036,854,775,808 to +9,233,372,036,854,775,807
    return [Row.replace('^BIGINT$', GenSecretRamdonDigitData(0, +9233372036854775807), 1) for Row in SrcRow] 


def GenDecimalData(SrcRow)->list:
    reg = re.compile(r'\^DECIMAL\$\((\d+\,\d+)')
    re_match = reg.findall(','.join(SrcRow))
    
    for Decimallength in re_match:
        IntLen, FloatLen = Decimallength.split(',')
        SrcRow = [Row.replace('^DECIMAL$('+Decimallength+')', GenRandomNumeric(IntLen, FloatLen),1) for Row in SrcRow]

    ConvertRow = SrcRow
    return ConvertRow 

def GenRandomNumeric(IntLen, FloatLen)->str:
    strRandomDecimal = GenSecretRamdonDigitData(0,int('9' * int(IntLen)))
    if int(FloatLen) != 0:
        return strRandomDecimal[:(int(IntLen)-int(FloatLen))*1]+'.'+strRandomDecimal[int(FloatLen)*-1:]
    elif (int(FloatLen) == 0):
        return strRandomDecimal[:(int(IntLen)-int(FloatLen))*1]
    elif(int(IntLen) == int(FloatLen)):
        return '.'+ strRandomDecimal[int(FloatLen)*-1:]

def GenNumericData(SrcRow)->list:
    reg = re.compile(r'\^NUMERIC\$\((\d+\,\d+)')
    re_match = reg.findall(','.join(SrcRow))
    
    for Decimallength in re_match:
        IntLen, FloatLen = Decimallength.split(',')
        SrcRow = [Row.replace('^NUMERIC$('+Decimallength+')', GenRandomNumeric(IntLen, FloatLen),1) for Row in SrcRow]

    ConvertRow = SrcRow
    return ConvertRow 


def GenFloatData(SrcRow)->list:
    # Teradata : https://docs.teradata.com/r/WurHmDcDf31smikPbo9Mcw/RhAF_5yskR0MQJyrFVcSxQ
    # Represent values in sign/magnitude form ranging from 2.226 x 10-308 to 1.797 x 10308.

    return [Row.replace('^FLOAT$', GenRandomNumeric(6, 3),1) for Row in SrcRow]

def GenCharData(SrcRow)->list:
    reg = re.compile(r'\^CHAR\$\((\d+)', re.VERBOSE | re.IGNORECASE| re.MULTILINE | re.DOTALL)
    re_match = filter(reg.match, SrcRow)
    ConvertRow = SrcRow

    for Varlength in re_match:
        strRandomVarchar = GenSecretRamdonTextData(int(Varlength.replace('^CHAR$(','').replace(')','')))
        ConvertRow = list(map(lambda item: item.replace(Varlength,strRandomVarchar,1), ConvertRow))            

    return ConvertRow   

def GenVarcharData(SrcRow)->list:
    reg = re.compile(r'\^VARCHAR\$\((\d+)', re.VERBOSE | re.IGNORECASE| re.MULTILINE | re.DOTALL)
    re_match = filter(reg.match, SrcRow)
    ConvertRow = SrcRow
    
    for Varlength in re_match:
        strRandomVarchar = GenSecretRamdonTextData(int(Varlength.replace('^VARCHAR$(','').replace(')','')))
        ConvertRow = list(map(lambda item: item.replace(Varlength,strRandomVarchar,1), ConvertRow))
    
    return ConvertRow   

def GenDateData(SrcRow)->list:
    #"%H%M%S"
    return list(map(lambda x: str.replace(x, "^DATE$", str((datetime.datetime.now()+ datetime.timedelta(days=int(GenSecretRamdonDigitData(-10, 10)))).strftime("%Y%m%d")),1), SrcRow))
   
def GenTimeData(SrcRow)->list:
    #HHMMSS.nnnnnn
    return list(map(lambda x: str.replace(x, "^TIME$", str((datetime.datetime.now()+ datetime.timedelta(hours=int(GenSecretRamdonDigitData(-100, 100)))).strftime("%H%M%S")+'.'+GenSecretRamdonDigitData(0, 9)*6),1), SrcRow))


def GenTimestampData(SrcRow)->list:
    #YYMMDDHHMMSS.nnnnnn
    return list(map(lambda x: str.replace(x, "^TIMESTAMP$", str((datetime.datetime.now()+ datetime.timedelta(hours=int(GenSecretRamdonDigitData(-100, 100)))).strftime("%Y%m%d%H%M%S")+'.'+GenSecretRamdonDigitData(0, 9)*6),1), SrcRow))

def flatten(lis):
    ''' Multiple Dimension List Convert to 1-Dimension List '''

    for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item