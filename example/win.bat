@echo off

copy filesize.bat ..
cd ..
call filesize.bat
del filesize.bat
move filesizes.dat example
cd subdirectory

py ../visualization.pyw filesizes.dat
