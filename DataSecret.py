import string
import sys

class DataSecretClass:
    def __init__(self, Dtype):
        self.Dtype = ''
    @staticmethod
    def CheckSecurityInput(SrcInput:string)->string:
        BlackList = ["--", ";--", ";", "/*", "*/", "@@", 
                    "@", "CHAR", "NCHAR", "VARCHAR", "NVARCHAR", "ALTER", 
                    "BEGIN", "CAST", "CREATE", "CURSOR", "DECLARE", "DELETE", 
                    "DROP", "END", "EXEC", "EXECUTE", "FETCH", "INSERT", 
                    "KILL", "OPEN", "SELECT", "SYS", "SYSOBJECTS", "SYSCOLUMNS", 
                    "TABLE", "UPDATE", "UPDATE.TXT"]
        if SrcInput.upper() in BlackList : 
            print('程式帶入資料路徑異常, 請再修正 : '+SrcInput)
            sys.exit() 
        return SrcInput