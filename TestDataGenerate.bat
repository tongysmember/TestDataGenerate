@echo off
echo 測試資料產生器
echo ===============================================================

:CheckDdlFile
	set /p DdlPath=請輸入來源DDL檔案路徑(DDL資料夾當中檔案):
	set "DdlPath=./DDL/%DdlPath%"
	echo %DdlPath%


:CheckHeader
	set /p BoolHeader=是否需要表頭Header[Y/N]:
	echo %BoolHeader%
	set BoolHeaderInput=False

	IF %BoolHeader% == Y set "BoolHeaderInput=True"
	IF %BoolHeader% == y set "BoolHeaderInput=True"
	IF %BoolHeader% == N set "BoolHeaderInput=True"
	IF %BoolHeader% == n set "BoolHeaderInput=True"
	IF NOT %BoolHeaderInput%==True (
		ECHO 請輸入[Y/N]
		GOTO CheckHeader
	)
:CheckTailer
	set /p BoolTailer=是否需要表尾Tailer[Y/N]:
	echo %BoolTailer%
	set BoolTailerInput=False

	IF %BoolTailer% == Y set "BoolTailerInput=True"
	IF %BoolTailer% == y set "BoolTailerInput=True"
	IF %BoolTailer% == N set "BoolTailerInput=True"
	IF %BoolTailer% == n set "BoolTailerInput=True"
	IF NOT %BoolTailerInput%==True (
		ECHO 請輸入[Y/N]
		GOTO CheckTailer
	)

:CheckCNT
	set /p IntRows=資料產生筆數(正整數):
	echo %IntRows%
	set BoolIntRowsInput=False
	
	SET "var="&for /f "delims=0123456789" %%i in ("%IntRows%") do set var=%%i
	if defined var (set "BoolIntRowsInput=False") else (set "BoolIntRowsInput=True")

	IF NOT %BoolIntRowsInput%==True (
		ECHO 請輸入大於 0 整數
		GOTO CheckCNT
	)


echo 執行程式 

py -3.8 TestDataGenerate.py %BoolHeader% %BoolTailer% %IntRows% %DdlPath%

pause 