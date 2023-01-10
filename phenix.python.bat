@setlocal
@set LIBTBX_BUILD=%~dp0
@set LIBTBX_BUILD=%LIBTBX_BUILD:~0,-1%
@for %%F in ("%LIBTBX_BUILD%") do @set LIBTBX_BUILD=%%~dpF
@set LIBTBX_BUILD=%LIBTBX_BUILD:~0,-1%
@set LIBTBX_DISPATCHER_NAME=%~nx0
@set PYTHONPATH=%LIBTBX_BUILD%\..\modules;%LIBTBX_BUILD%\..\modules\phenix;%LIBTBX_BUILD%\..\modules\phenix_pathwalker;%LIBTBX_BUILD%\..\modules\reel;%LIBTBX_BUILD%\..\modules\cctbx_project;%LIBTBX_BUILD%\..\modules\elbow;%LIBTBX_BUILD%\..\modules\PyQuante;%LIBTBX_BUILD%\..\modules\phaser;%LIBTBX_BUILD%\..\modules\tntbx;%LIBTBX_BUILD%\..\modules\cctbx_project\boost_adaptbx;%LIBTBX_BUILD%\lib;%LIBTBX_BUILD%\..\conda_base\lib\site-packages;%LIBTBX_BUILD%\..\conda_base;%PYTHONPATH%
@set PATH=%LIBTBX_BUILD%\lib;%PATH%
@set PATH=%LIBTBX_BUILD%\bin;%LIBTBX_BUILD%\..\conda_base\Library\bin;%PATH%
@set LIBTBX_PYEXE=%LIBTBX_BUILD%\..\conda_base\python.exe
@REM -----------------------------------------------------------------------------------------------------------------------------------------------------------------
@REM included from c:\users\bkpoon\slave\phenix-nightly-intel-windows-x86_64\tmp\phenix-installer-1.20.1-4487-intel-windows-x86_64\build\dispatcher_include_phenix.bat
@set PHENIX="C:\Users\BKPoon\slave\phenix-nightly-intel-windows-x86_64\tmp\phenix-installer-1.20.1-4487-intel-windows-x86_64"
@set PHENIX_VERSION=1.20.1-4487
@set PHENIX_ENVIRONMENT=1
@set PHENIX_MTYPE=intel-windows-x86_64
@
@REM -----------------------------------------------------------------------------------------------------------------------------------------------------------------
@"%LIBTBX_PYEXE%" -Qnew %*
