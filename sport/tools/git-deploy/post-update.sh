#!/bin/sh
#
# An example hook script to prepare a packed repository for use over
# dumb transports.
#
# To enable this hook, rename this file to "post-update".

unset GIT_DIR
LOG_FILE="~/logs/swd/git.log"
PROJECT="street-workout-database"
PROJECT_DIR=~/projects/swd/

echo "**** Pulling changes into Live [Hub's post-update hook]" >> $LOG_FILE
echo "Starting at: `date`" >> $LOG_FILE

if [ ! -d "$PROJECT_DIR" ]; then
    virtualenv-3.2 $PROJECT_DIR
    git clone -b release-v1.1 ~/git/swd.git $PROJECT_DIR$PROJECT
fi

cd $PROJECT_DIR$PROJECT || exit
git pull origin

echo "Finish at: `date`" >> $LOG_FILE
exec git update-server-info
