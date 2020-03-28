echo off
start /min cmd /c "echo off&&python HTTPServer.py"
start /max cmd /c "echo off&&python index.py --log --debug --show --upload http://localhost:8010/ --min-eyes 1 --max-eyes 3"