#!/bin/bash
source ../bin/activate
echo starting celery
celery -A tasks worker --beat --loglevel=info
