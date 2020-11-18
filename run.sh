#!/usr/bin/zsh

if lsof -i:5001
then
    sudo kill -9 $(sudo lsof -t -i:5001)
fi

if lsof -i:6380
then
    sudo kill -9 $(sudo lsof -t -i:6380)
fi

redis-server --port 6380 &
sleep 1s

python3 worker.py &
sleep 1s

if [ -z "$1" ]
then
    HOST='0.0.0.0'
else
    HOST=$1
fi

flask run --port=5001 --host=$HOST &
