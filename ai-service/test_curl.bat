@echo off
echo ================================
echo AI Art Service - Quick Curl Test
echo ================================

echo.
echo 1. Testing Health Endpoint...
curl -s "http://localhost:8080/health" | echo.

echo.
echo 2. Testing Image Generation...
echo Generating image with prompt: "a small cat"
curl -X POST "http://localhost:8080/generate" ^
     -H "Content-Type: application/json" ^
     -d "{\"prompt\": \"a small cat\", \"steps\": 5}" ^
     --max-time 120

echo.
echo Test completed!