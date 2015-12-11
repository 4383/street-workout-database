#!/bin/sh
#
# An example hook script to prepare a packed repository for use over
# dumb transports.
#
# To enable this hook, rename this file to "post-update".

unset GIT_DIR
LOG_FILE="/home/`whoami`/logs/swd/git.log"
LOGERROR_FILE="/home/`whoami`/logs/swd/git.error.log"
PROJECT="street-workout-database"
PROJECTDIR=/home/`whoami`/projects/swd
PROJECTLOGDIR=/home/`whoami`/logs/swd
SOCKETDIR=/home/`whoami`/sockets/swd
DJANGODIR=$PROJECTDIR/street-workout-database/sport/web
GUNICORN=$PROJECTDIR/$PROJECT/sport/tools/server/gunicorn/gunicorn.sh

echo "**** Pulling changes into Live [Hub's post-update hook]" >> $LOG_FILE
echo "Starting at: `date`" >> $LOG_FILE

supervisorctl stop swd_`whoami`

if [ -d "$PROJECTDIR" ]; then
    rm -rf $PROJECTDIR
fi

if [ -d $PROJECTLOGDIR ]; then
    rm -rf $PROJECTLOGDIR
    touch $PROJECTLOGDIR/gunicorn_supervisor.log
fi

if [ -d $SOCKETDIR ]; then
    rm -rf $SOCKETDIR
    mkdir -p $SOCKETDIR/run
fi

virtualenv-3.2 $PROJECTDIR 2>> $LOGERROR_FILE
git clone -b `whoami` /home/`whoami`/git/`whoami`.swd.git $PROJECTDIR/$PROJECT 2>> $LOGERROR_FILE

cd $PROJECTDIR/$PROJECT || exit

source $PROJECTDIR/bin/activate 2>> $LOGERROR_FILE
$PROJECTDIR/bin/pip install -r $PROJECTDIR/$PROJECT/sport/fixtures/`whoami`.requirements.txt 2>> $LOGERROR_FILE

cd $DJANGODIR

python manage.py makemigrations 2>> $LOGERROR_FILE
python manage.py migrate 2>> $LOGERROR_FILE
python manage.py collectstatic 2>> $LOGERROR_FILE

chmod +x $GUNICORN

supervisorctl start swd_`whoami`

echo "Finish at: `date`" >> $LOG_FILE
exec git update-server-info
