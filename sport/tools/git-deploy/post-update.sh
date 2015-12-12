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
WWWDIR=/home/`whoami`/www/swd
DJANGODIR=$PROJECTDIR/street-workout-database/sport/web
GUNICORN=$PROJECTDIR/$PROJECT/sport/tools/server/gunicorn/gunicorn.sh

function rollback () {
    git reset $CURRENT_REVISION
    $PROJECTDIR/bin/python manage.py collectstatic --clear --noinput
    $PROJECTDIR/bin/python manage.py makemigrations
    $PROJECTDIR/bin/python manage.py migrate
    chmod +x $GUNICORN
    supervisorctl start swd_`whoami`
}

echo "**** Pulling changes into Live [Hub's post-update hook]" >> $LOG_FILE
echo "Starting at: `date`" >> $LOG_FILE

supervisorctl stop swd_`whoami`

if [ ! -d "$PROJECTDIR" ]; then
    virtualenv-3.2 $PROJECTDIR
    git clone -b `whoami` /home/`whoami`/git/`whoami`.swd.git $PROJECTDIR/$PROJECT
fi

if [ -d $PROJECTLOGDIR ]; then
    rm -rf $PROJECTLOGDIR
    mkdir $PROJECTLOGDIR
    touch $PROJECTLOGDIR/gunicorn_supervisor.log
fi

if [ -d $SOCKETDIR ]; then
    rm -rf $SOCKETDIR
    mkdir -p $SOCKETDIR/run
fi

cd $PROJECTDIR/$PROJECT || exit
CURRENT_REVISION=`git rev-parse HEAD`
git pull origin `whoami`

source $PROJECTDIR/bin/activate
$PROJECTDIR/bin/pip install -r $PROJECTDIR/$PROJECT/sport/fixtures/`whoami`.requirements.txt

cd $DJANGODIR

$PROJECTDIR/bin/python manage.py dumpdata > $WWWDIR/backup.json
if [ $? -eq 1 ]; then
    rollback
fi
$PROJECTDIR/bin/python manage.py collectstatic --clear --noinput
if [ $? -eq 1 ]; then
    rollback
fi
$PROJECTDIR/bin/python manage.py makemigrations
if [ $? -eq 1 ]; then
    rollback
fi
$PROJECTDIR/bin/python manage.py migrate
if [ $? -eq 1 ]; then
    rollback
fi

chmod +x $GUNICORN
supervisorctl start swd_`whoami`
ERROR_OCCURED=`supervisorctl status swd_\`whoami\` | grep 'STOPPED'`

# rollback if supervirsor start fail
if [ ! -z $ERROR_OCCURED ]; then
    if [ $? -eq 1 ]; then
        rollback
    fi
fi

echo "Finish at: `date`" >> $LOG_FILE
exec git update-server-info
