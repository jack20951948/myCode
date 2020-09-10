#!/bin/bash
cd ~/python
echo [INFO] Start program...
python3 pgv_test.py
echo [INFO] Stop program...
python3 stop_pgv.py
echo [INFO] Switch to Manual mode
python3 pgv_manual.py