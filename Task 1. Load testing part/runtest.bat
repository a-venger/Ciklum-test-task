@ECHO OFF
cd .\apache-jmeter-4.0
@RD /S /Q "..\results"
call bin\jmeter.bat -n -t "..\testplan\Deezer.jmx" -Jusers=50 -Jrampup=300 -Jduration=900 -l "..\results\testResult.csv" -j "..\results\jmeter.log" -e -o "..\results\Html" -f
call start chrome ..\results\Html\index.html
pause