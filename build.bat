@echo off
echo Installing PyInstaller...
pip install pyinstaller

echo Installing Windows 11 Theme Dependencies...
pip install sv_ttk darkdetect

echo Building the executable...
pyinstaller --noconsole --onefile "d:\AI_Technology\My Tools\watermark_app\watermark_studio.py"

echo.
echo Build complete! Check the 'dist' folder for your watermark_studio.exe.
pause