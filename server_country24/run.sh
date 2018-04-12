#!/bin/sh
cd /root/crawler-1.0/server_country24
for i in `ps aux | grep run.py|awk '{print $2;}'`;do kill -9 $i;done;
/root/crawler-1.0/country24_env/bin/python /root/crawler-1.0/server_country24/run.py
