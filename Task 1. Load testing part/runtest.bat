cd .\apache-jmeter-4.0
set /p users=Enter number of users:
set /p rampup=Enter rampup: 
set /p duration=Enter duration: 
@RD /S /Q "..\results"
call bin\jmeter.bat -n -t "..\testplan\Deezer.jmx" -Jusers=%users% -Jrampup=%Jrampup% -Jduration=%duration% -l "..\results\testResult.csv" -j "..\results\jmeter.log" -e -o "..\results\Html" -f

SET LookForFile="..\results\Html\index.html"

:CheckForFile
IF EXIST %LookForFile% GOTO OpenReport
TIMEOUT /T 5 >nul

GOTO CheckForFile

:OpenReport
call start ..\results\Html\index.html

pause