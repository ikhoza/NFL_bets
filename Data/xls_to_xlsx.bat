@echo off

:: Set the current directory to the location of the batch file
setlocal
set "script_dir=%~dp0"

:: Define the directories relative to the script location
set "xls_directory=%script_dir%temp"
set "xlsx_directory=%script_dir%Files"

:: Create the output directory if it doesn't exist
if not exist "%xlsx_directory%" mkdir "%xlsx_directory%"

:: Loop through each .xls file in the directory
for %%F in ("%xls_directory%\*.xls") do (
    if not exist "%xlsx_directory%\%%~nF.xlsx" (
        echo Converting "%%~nxF"...
        "C:\Program Files\LibreOffice\program\soffice.exe" --convert-to xlsx --outdir "%xlsx_directory%" "%%F"
    )
)

echo Conversion complete.

exit
