echo off
start /min cmd /c "echo off&&python src/HTTPServer.py"
start /max cmd /c "echo off&&python src/main.py--log --show --debug --upload http://localhost:8010/ --min-eyes 1 --max-eyes 3"
