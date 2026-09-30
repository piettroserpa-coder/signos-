@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AstroSign - Servidor

echo ==========================================
echo       ASTROSIGN - INICIANDO SITE
echo ==========================================
echo.

where py >nul 2>nul
if errorlevel 1 (
  echo [ERRO] Python nao encontrado.
  echo Instale o Python e marque a opcao "Add Python to PATH".
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [1/3] Criando ambiente virtual...
  py -m venv .venv
)

call ".venv\Scripts\activate.bat"
echo [2/3] Instalando dependencias...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo [ERRO] Nao foi possivel instalar as dependencias.
  pause
  exit /b 1
)

echo [3/3] Abrindo http://127.0.0.1:5000
echo.
start "" http://127.0.0.1:5000
python app.py
pause
