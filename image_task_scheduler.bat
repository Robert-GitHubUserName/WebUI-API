@echo on
REM === Scheduled batch file for automated image generation ===
REM Uses a daily queue file and Python script to process tasks

REM -- Set date string for today (YYYYMMDD)
for /f %%a in ('wmic os get localdatetime ^| find "."') do set datetime=%%a
set today=%datetime:~0,8%

REM -- Define working directories (edit as needed)
set SCRIPTDIR=D:\Files\Code\Python\WebUI-API
set QUEUEFILE=%SCRIPTDIR%\image_tasks_new_%today%.txt
set DONEFILE=%SCRIPTDIR%\image_tasks_done_%today%.txt

REM -- Call Python script to process today’s queue file
REM   (Python script should handle moving lines from new to done)
"C:\Program Files\Python311\python.exe" "%SCRIPTDIR%\image_task_batch_runner.py" --queue "%QUEUEFILE%" --done "%DONEFILE%"

REM -- Optionally, log completion timestamp
>> "%SCRIPTDIR%\batch_run.log" echo Completed run on %date% at %time%

echo Image batch generation complete.
