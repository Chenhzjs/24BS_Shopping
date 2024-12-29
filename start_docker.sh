#!/bin/bash

./environment.sh
cd /work/web
./web_start.sh &
cd /work/server
python3 core.py &
python3 detail.py &

# mysql -u root -h 127.0.0.1
