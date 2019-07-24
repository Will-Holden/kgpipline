#!/bin/bash

basepath=$(cd `dirname $0`; pwd)
HOME=$(cd $basepath/..;pwd)
APP_PID=$HOME/pid/pid.txt

start_worker(){
    celery multi start w1 -A piplinecelery -l info
}

start_master(){
    cd $HOME/
    nohup python main.py > logs/nohup.out 2>&1 &
    echo $!>$APP_PID
    echo "starting at pid"$(cat $APP_PID)
}

stop_worker(){
    celery multi stop w1
}

stop_master(){
    echo "stopping pid"$(cat $APP_PID)
    sudo kill -9 $(cat $APP_PID)
}

case $1 in
    start_worker)
        start_worker
        ;;
    start_master)
        start_master
        ;;
    stop_master)
        stop_master
        ;;
    stop_worker)
        stop_worker
        ;;
    *)
        echo "Usage:{start_worker|start_master|stop_worker|stop_master}"
        ;;
esac
exit 0
