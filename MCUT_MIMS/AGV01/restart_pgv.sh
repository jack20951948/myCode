#!/bin/bash
pgv_py_data=$(ps -ef | grep python3 | grep pgv.py )
index_of_py=$(echo $pgv_py_data| cut -d " " -f 2)
echo Searching program \"pgv.py\"...
if [ -n "$index_of_py" ]
then
    echo Killing pgv process id:$index_of_py
    kill -9 $index_of_py
    echo Restart the program!
else
    echo Error!!! Please reboot the robot...
fi