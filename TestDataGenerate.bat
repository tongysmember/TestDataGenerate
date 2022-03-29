@echo off
echo 測試資料產生器
echo ===============================================================

set /p DdlPath=請輸入來源DDL路徑(DDL資料夾):
echo %DdlPath%

IF EXIST %DdlPath% (
  echo 檔案存在
) ELSE (
  echo 檔案不存在, 請重新輸入
)

set /p BoolHeader=是否需要表頭Header(Y, N):
echo %BoolHeader%

set /p BoolTailer=是否需要表尾Tailer(Y, N):
echo %BoolTailer%

set /p IntRows=資料產生筆數(正整數):
echo %IntRows%

echo 執行程式 

py -3.8 TestDataGenerate_class.py %BoolHeader% %BoolTailer% %IntRows%

pause