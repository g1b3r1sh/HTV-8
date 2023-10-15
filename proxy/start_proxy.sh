#!/bin/bash

source venv/bin/activate
python3 proxy.py &
python3 distributed-server-controller.py &
