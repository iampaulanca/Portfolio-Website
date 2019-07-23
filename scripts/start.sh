#!/bin/bash

cd /home/ec2-user/
killall python
killall python3
sudo /etc/init.d/mysqld start
source venv/bin/activate py36
python3 run.py > /dev/null 2> /dev/null < /dev/null &
