@echo off
net session >nul 2>&1
if %errorLevel% == 0 (
    cd "C:\tools\dns-changer\"
    python "C:\tools\dns-changer\dns-changer.py" %*
) else (
    echo ⚠ Requesting Administrator privileges...
    powershell -Command "\c Start-Process cmd -ArgumentList '\"%~f0 %*\"' -Verb RunAs"
    exit
)
