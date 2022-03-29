@echo off
echo ���ո�Ʋ��;�
echo ===============================================================

set /p DdlPath=�п�J�ӷ�DDL���|(DDL��Ƨ�):
echo %DdlPath%

IF EXIST %DdlPath% (
  echo �ɮצs�b
) ELSE (
  echo �ɮפ��s�b, �Э��s��J
)

set /p BoolHeader=�O�_�ݭn���YHeader(Y, N):
echo %BoolHeader%

set /p BoolTailer=�O�_�ݭn����Tailer(Y, N):
echo %BoolTailer%

set /p IntRows=��Ʋ��͵���(�����):
echo %IntRows%

echo ����{�� 

py -3.8 TestDataGenerate.py %BoolHeader% %BoolTailer% %IntRows%

pause