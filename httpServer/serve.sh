#!/bin/bash
cd $1
nohup /usr/bin/python3 -m http.server 80 >/dev/null 2>&1 &
cd ..
cd ..
nohup /usr/bin/python3 Agente.py >/dev/null 2>&1 &

