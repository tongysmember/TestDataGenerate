# TestDataGenerate 測資產生程式

## 程式運行
python3 TestDataGenerate.py %BoolHeader% %BoolTailer% %IntRows% %DdlPath%

%BoolHeader% => 是否輸出表頭 
%BoolTailer% => 是否輸出表尾(顯示筆數)
%IntRows% => 總行數
%DdlPath% => 參考 DDL規格 檔案

## DDL 資料欄位參考

https://www.tutorialspoint.com/teradata/teradata_data_types.htm

| Data Types | Length (Bytes) | Range of values                                            |
|------------|----------------|------------------------------------------------------------|
| BYTEINT    | 1              | -128 to +127                                               |
| SMALLINT   | 2              | -32768 to +32767                                           |
| INTEGER    | 4              | -2,147,483,648 to +2147,483,647                            |
| BIGINT     | 8              | -9,233,372,036,854,775,80 8 to +9,233,372,036,854,775,8 07 |
| DECIMAL    | 1-16           |                                                            |
| NUMERIC    | 1-16           |                                                            |
| FLOAT      | 8              | IEEE format                                                |
| CHAR       | Fixed Format   | 1-64,000                                                   |
| VARCHAR    | Variable       | 1-64,000                                                   |
| DATE       | 4              | YYYYYMMDD                                                  |
| TIME       | 6 or 8         | HHMMSS.nnnnnn or HHMMSS.nnnnnn+HHMM                        |
| TIMESTAMP  | 10 or 12       | YYMMDDHHMMSS.nnnnnn or YYMMDDHHMMSS.nnnnnn +HHMM           |


---
Todo: 

1. Add Setting.cfg => Data Type Uppper/Lower Bound
2. DDL Column 數量檢查
3. Main.py and Classes Folder
4. Fix Length d

---


# Ref:
## Regex DDL Script
1. https://stackoverflow.com/questions/54626068/python-regex-fetching-column-details-from-ddl 

1. https://regex101.com/r/jcCBch/1/

1. https://pythex.org/
