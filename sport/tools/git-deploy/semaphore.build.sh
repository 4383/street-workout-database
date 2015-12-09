#!/usr/bin/env bash
#
# Use this script for automated test and check on application
#
# Used on semaphore.ci for automated build
#
pip install -r sport/server/staging.requirements.txt
cd sport/web/
python manage.py test
python manage.py check