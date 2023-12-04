@echo off
title 
:start
cls
pyinstaller -F -i "src/resources/image/icon.ico" src/main.py
del main.spec
rd build /s /q
pause
goto start