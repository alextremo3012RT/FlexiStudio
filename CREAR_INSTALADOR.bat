@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
title Flexi Studio - Generar instalador Windows

echo ==================================================
echo       FLEXI STUDIO - INSTALADOR DE WINDOWS
echo ==================================================
echo.
if not "%OS%"=="Windows_NT" (
  echo ERROR: este proceso se debe ejecutar en Windows.
  pause
  exit /b 1
)
where py >nul 2>&1
if errorlevel 1 (
  echo ERROR: instala Python 3.11 a 3.14 de 64 bits con el lanzador py.
  pause
  exit /b 1
)

if not exist ".venv-build\Scripts\python.exe" (
  echo [1/4] Creando entorno de compilacion...
  py -3 -m venv ".venv-build"
  if errorlevel 1 goto ERROR
)
set "PYTHON=%~dp0.venv-build\Scripts\python.exe"
echo [2/4] Instalando dependencias...
"%PYTHON%" -m pip install --upgrade pip
if errorlevel 1 goto ERROR
"%PYTHON%" -m pip install -r requirements.txt "pyinstaller>=6.17,<7"
if errorlevel 1 goto ERROR

echo [3/4] Preparando ejecutable para Windows...
"%PYTHON%" -m PyInstaller --noconfirm --clean "FlexiStudio.spec"
if errorlevel 1 goto ERROR
if not exist "dist\FlexiStudio\FlexiStudio.exe" goto ERROR

echo [4/4] Buscando Inno Setup 6...
set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not defined ISCC if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not defined ISCC for /f "delims=" %%I in ('where ISCC.exe 2^>nul') do if not defined ISCC set "ISCC=%%I"
if not defined ISCC (
  echo.
  echo FALTA INNO SETUP 6. Ya esta creado el programa portable en:
  echo dist\FlexiStudio\FlexiStudio.exe
  echo Instala Inno Setup 6 desde https://jrsoftware.org/isinfo.php
  echo y vuelve a ejecutar este archivo.
  pause
  exit /b 2
)
"%ISCC%" "FlexiStudio_Instalador.iss"
if errorlevel 1 goto ERROR

echo.
echo LISTO: instalador disponible en:
echo %CD%\salida\FlexiStudio_Setup_1.1.0.exe
echo.
echo Ejecutalo para instalar Flexi Studio.
pause
exit /b 0

:ERROR
echo.
echo No se pudo completar la compilacion.
echo Revisa el mensaje de error superior y enviamelo.
pause
exit /b 1
