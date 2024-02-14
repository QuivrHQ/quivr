#!/bin/bash

SESSION_NAME="my_services"

start_services() {
    # Create a new tmux session
    tmux new-session -d -s $SESSION_NAME

    # Split the window into panes for each service
    tmux split-window -h
    tmux split-window -v
    tmux select-pane -t 0
    tmux split-window -v

    # Start each service in its pane
    tmux send-keys -t $SESSION_NAME:0.0 'echo "Starting backend-core...";pipenv run uvicorn main:app --reload --host 0.0.0.0 --port 5050 --workers 6' C-m
    tmux send-keys -t $SESSION_NAME:0.1 'echo "Starting worker...";pipenv run celery -A celery_worker worker -l info' C-m
    tmux send-keys -t $SESSION_NAME:0.2 'echo "Starting beat...";pipenv run celery -A celery_worker beat -l info' C-m
    tmux send-keys -t $SESSION_NAME:0.3 'echo "Starting flower...";pipenv run celery -A celery_worker flower -l info --port=5555' C-m

    echo "Services started in tmux session '$SESSION_NAME'"
    echo "Use 'tmux attach-session -t $SESSION_NAME' to view logs"
}

stop_services() {
    # Kill the tmux session
    tmux kill-session -t $SESSION_NAME
    echo "Services stopped"
}

view_logs() {
    # Attach to the tmux session to view logs
    tmux attach-session -t $SESSION_NAME
}

if [ "$1" == "start" ]; then
    start_services
elif [ "$1" == "stop" ]; then
    stop_services
elif [ "$1" == "logs" ]; then
    view_logs
else
    echo "Usage: $0 {start|stop|logs}"
fi
