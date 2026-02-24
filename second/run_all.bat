@echo off
pushd "D:\3rd Year 2nd semester\Digital Image and Speech  Sessional\image"
python first.py
if %errorlevel% neq 0 pause
python second.py
if %errorlevel% neq 0 pause
popd
