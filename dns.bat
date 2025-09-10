@echo off
:: چک کردن دسترسی ادمین
net session >nul 2>&1
if %errorLevel% == 0 (
    python ".\dns-changer.py" %*
) else (
    echo ⚠ Requesting Administrator privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"%~f0\"' -Verb RunAs"
    python ".\dns-changer.py" %*
)


