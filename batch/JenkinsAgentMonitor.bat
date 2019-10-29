@ECHO off
SET ServiceName="jenkinsslave-D__Jenkins"
FOR /F "tokens=2-8 delims=.:/ " %%a IN ("%DATE% %TIME%") DO SET DateTime=%%c-%%a-%%b_%%d-%%e-%%f.%%g

NET START | FINDSTR %ServiceName%
IF %ERRORLEVEL% EQU 0 (
    REM ECHO [%DateTime%] Service running. ERRORLEVEL=%ERRORLEVEL%"
    ECHO [%DateTime%] Service running. >> %~n0.log
) ELSE (
    REM ECHO [%DateTime%] Service not running. ERRORLEVEL=%ERRORLEVEL%
    ECHO [%DateTime%] Service not running. >> %~n0.log
    NET START %ServiceName% >> %~n0.log
)
