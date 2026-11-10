@echo off
title Vagen-match dev server

echo.
echo  Starter Vagen-match (DEV MODE - ingen database nodvendig)...
echo  Apne nettleseren og ga til: http://127.0.0.1:5000
echo.
echo  Trykk CTRL+C for a stoppe serveren.
echo.

set DEV_MODE=1
uv run app.py

pause
