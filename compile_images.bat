@echo off
title 
cd src/resources
:start
cls
pyrcc5 -o image_data.py image/all.qrc 
pause
goto start