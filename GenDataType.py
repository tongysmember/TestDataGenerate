#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import datetime
import string
import random
from collections.abc import Iterable
import re
from DataTypeEnum import DataType

def GenDataType(SrcDataType,SrcRow):
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

def GenByteintData(SrcRow)->list:
    #-128 to +127
    return [Row.replace('BYTEINT', str(random.randint(0, +127))) for Row in SrcRow] 

def GenSmallintData(SrcRow)->list:
    #-32768 ~ +32767
    return [Row.replace('SMALLINT', str(random.randint(0 , +32767))) for Row in SrcRow] 

def GenIntegerData(SrcRow)->list:
    #-2,147,483,648 ~ +2,147,483,647
    return [Row.replace('INTEGER', str(random.randint(0, 2147483647))) for Row in SrcRow] 

def GenBigintData(SrcRow)->list:
    #-9,233,372,036,854,775,808 to +9,233,372,036,854,775,807
    return [Row.replace('BIGINT', str(random.randint(0 , +9233372036854775807))) for Row in SrcRow] 

def GenDecimalData(SrcRow)->list:
    reg = re.compile(r'DECIMAL\((\d+\,\d+)')
    re_match = reg.findall(','.join(SrcRow))
    
    for Decimallength in re_match:
        IntLen, FloatLen = Decimallength.split(',')
        strRandomDecimal = str(random.randint(0,int('9' * int(IntLen))))
        strRandomDecimal = strRandomDecimal[:int(IntLen)*-1]+'.'+strRandomDecimal[int(FloatLen)*-1:]
        SrcRow = [Row.replace('DECIMAL('+Decimallength+')', strRandomDecimal) for Row in SrcRow]

    ConvertRow = SrcRow
    return ConvertRow 

def GenNumericData(SrcRow)->list:
    reg = re.compile(r'NUMERIC\((\d+\,\d+)')
    re_match = reg.findall(','.join(SrcRow))
    
    for Decimallength in re_match:
        IntLen, FloatLen = Decimallength.split(',')
        strRandomDecimal = str(random.randint(0,int('9' * int(IntLen))))
        if int(FloatLen) != 0:
            strRandomDecimal = strRandomDecimal[:(int(IntLen)-int(FloatLen))*1]+'.'+strRandomDecimal[int(FloatLen)*-1:]
        elif (int(FloatLen) == 0):
            strRandomDecimal = strRandomDecimal[:(int(IntLen)-int(FloatLen))*1]
        elif(int(IntLen) == int(FloatLen)):
            strRandomDecimal = '.'+ strRandomDecimal[int(FloatLen)*-1:]

        SrcRow = [Row.replace('NUMERIC('+Decimallength+')', strRandomDecimal) for Row in SrcRow]

    ConvertRow = SrcRow
    return ConvertRow 

def GenFloatData(SrcRow)->list:
    # Teradata : https://docs.teradata.com/r/WurHmDcDf31smikPbo9Mcw/RhAF_5yskR0MQJyrFVcSxQ
    # Represent values in sign/magnitude form ranging from 2.226 x 10-308 to 1.797 x 10308.

    return [Row.replace('FLOAT', str(random.uniform(0, +999.999))) for Row in SrcRow] 

def GenCharData(SrcRow)->list:
    reg = re.compile(r'^CHAR\((\d+)', re.VERBOSE | re.IGNORECASE| re.MULTILINE | re.DOTALL)
    re_match = filter(reg.match, SrcRow)
    ConvertRow = SrcRow

    for Varlength in re_match:
        strRandomVarchar = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(int(Varlength.replace('CHAR(','').replace(')',''))))
        
        index =0
        for Col in SrcRow:            
            if  'CHAR' in Col  and 'VARCHAR' not in Col:
                ConvertRow[index] = Col.replace( Varlength , strRandomVarchar )
                index +=1
            else :
                index +=1
                continue
    return ConvertRow   

def GenVarcharData(SrcRow)->list:
    reg = re.compile(r'^VARCHAR\((\d+)', re.VERBOSE | re.IGNORECASE| re.MULTILINE | re.DOTALL)
    re_match = filter(reg.match, SrcRow)
    ConvertRow = SrcRow
    
    for Varlength in re_match:
        strRandomVarchar = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(int(Varlength.replace('VARCHAR(','').replace(')',''))))
        
    ConvertRow = list(map(lambda item: item.replace(Varlength,strRandomVarchar), ConvertRow))
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

def flatten(lis):
    ''' Multiple Dimension List Convert to 1-Dimension List '''

     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item