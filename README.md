# TestDataGenerate 測資產生程式

## 資料欄位參考

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