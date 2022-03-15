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



---

# Git Comment Type
- Added ( 新加入的需求 )
- Fixed ( 修复 bug )
- Changed ( 完成的任务 )
- Updated ( 完成的任务，或者由于第三方模块变化而做的变化 )
- feat: 新增/修改功能 (feature)。
- fix: 修補 bug (bug fix)。
- docs: 文件 (documentation)。
- style: 格式 (不影響程式碼運行的變動 white-space, formatting, missing semi colons, etc)。
- refactor: 重構 (既不是新增功能，也不是修補 bug 的程式碼變動)。
- perf: 改善效能 (A code change that improves performance)。
- test: 增加測試 (when adding missing tests)。
- chore: 建構程序或輔助工具的變動 (maintain)。
- revert: 撤銷回覆先前的 commit 例如：revert: type(scope): subject (回覆版本：xxxx)。

---

# Ref:
## Regex DDL Script
1. https://stackoverflow.com/questions/54626068/python-regex-fetching-column-details-from-ddl 

1. https://regex101.com/r/jcCBch/1/

1. https://pythex.org/
