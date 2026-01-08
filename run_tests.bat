@echo off
REM Test Execution Script - Tum testleri calistirir ve rapor olusturur (Playwright)

echo ========================================
echo Kamile Sor Test Otomasyonu (Playwright)
echo ========================================
echo.

REM Cache temizle
echo Cache temizleniyor...
if exist __pycache__ rmdir /S /Q __pycache__
if exist pages\__pycache__ rmdir /S /Q pages\__pycache__
if exist tests\__pycache__ rmdir /S /Q tests\__pycache__
if exist utils\__pycache__ rmdir /S /Q utils\__pycache__
echo Cache temizlendi!
echo.

REM Test raporu klasorunu olustur
if not exist "test-reports" mkdir test-reports

REM Playwright başlatıcı dosyasını yükle (gerekirse)
echo Playwright ortami kontrol ediliyor...
REM Testleri calistir
echo Testler calistiriliyor...
echo ----------------------------------------
py -m pytest tests/ -v -s --html=test-reports/test-report.html --self-contained-html

REM Sonuc
echo.
echo ========================================
echo Test tamamlandi!
echo Rapor: test-reports\test-report.html
echo ========================================
pause
