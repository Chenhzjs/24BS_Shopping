#!/bin/bash

./environment.sh
cd /work/web
/work/web/web_start.sh &
cd /work/server
python3 core.py &
python3 detail.py &
