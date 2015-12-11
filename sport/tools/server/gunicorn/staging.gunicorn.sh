#!/bin/bash

ENVIRONMENT=/home/`whoami`
NAME="swd_`whoami`"                                           # Name of the application
PROJECTDIR=$ENVIRONMENT/projects/swd
DJANGODIR=$PROJECTDIR/street-workout-database/sport/web         # Django project directory
SOCKFILE=$ENVIRONMENT/sockets/swd/run/gunicorn.sock             # we will communicte using this unix socket
LOGFILE=$ENVIRONMENT/logs/swd/gunicorn.log
STARTLOGFILE=$ENVIRONMENT/logs/swd/gunicorn.launch.log
USER=`whoami`                                                 # the user to run as
GROUP=webuser                                                   # the group to run as
NUM_WORKERS=3                                                   # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=sport.settings                           # which settings file should Django use
DJANGO_WSGI_MODULE=sport.wsgi                                   # WSGI module name
GUNICORNLOGDIR=$ENVIRONMENT/logs/swd/gunicorn.log

echo "*********************************************" >> $STARTLOGFILE
echo "Starting $NAME as `whoami`" >> $STARTLOGFILE
echo `date` >> $STARTLOGFILE

# Activate the virtual environment
cd $DJANGODIR
source $PROJECTDIR/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec $PROJECTDIR/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=info \
  --log-file=$GUNICORNLOGDIR
