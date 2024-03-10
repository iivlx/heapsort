@echo off
setlocal EnableDelayedExpansion

set "output="

for %%F in (*) do (
    set "output=!output! %%~zF"
)

:: Trim the leading space and write to filesizes.dat
echo %output:~1% > filesizes.dat

endlocal