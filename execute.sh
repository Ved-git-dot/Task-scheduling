#!/bin/bash
source ../bin/activate
celery -A tasks worker --beat --loglevel=info
