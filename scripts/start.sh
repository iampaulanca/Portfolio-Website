#!/bin/bash

cd /home/ec2-user/
source venv/bin/activate py36
python3 run.py > run.out 2> run.err &


