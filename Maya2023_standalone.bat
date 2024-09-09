@ECHO OFF
SETLOCAL

set PYMEL_SKIP_MEL_INIT=1
REM Assign arguments to variables 
set maya_file=%1
if "%~1"=="" (
	set /p maya_file=Enter the Maya file path to export FBX:
)
:: Display the inputs 
echo %maya_file% 
 
"c:/Program Files/Autodesk/Maya2023/bin/mayapy.exe" "stda_fbx_exporter_maya.py" --maya_file %maya_file% 
endlocal 
pause
:: ==================================================================