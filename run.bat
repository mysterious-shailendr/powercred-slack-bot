@REM For Windows Users

source venv/bin/activate

setlocal
for /f "delims=" %%A in (.env) do set %%A
endlocal

uvicorn src.main:app --reload