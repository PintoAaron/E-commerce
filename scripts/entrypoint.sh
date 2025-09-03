#!/bin/bash

celery -A Ecommerce worker --loglevel=info    --concurrency=4 --pool=redis -Q default