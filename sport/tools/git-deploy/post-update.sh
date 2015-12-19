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
ENVNAME=`whoami`

function rollback () {
    echo "rollback require" >> $LOG_FILE
    git checkout $CURRENT_REVISION
    $PROJECTDIR/bin/python manage.py collectstatic --clear --noinput
    $PROJECTDIR/bin/python manage.py makemigrations
    $PROJECTDIR/bin/python manage.py migrate
    chmod +x $GUNICORN
    supervisorctl start swd_`whoami`
    echo "rollback ok" >> $LOG_FILE
    echo "Finish at: `date`" >> $LOG_FILE
    exec git update-server-info
    exit
}

if [ -d $PROJECTLOGDIR ]; then
    rm -rf $PROJECTLOGDIR
    mkdir $PROJECTLOGDIR
    touch $PROJECTLOGDIR/gunicorn_supervisor.log
fi

echo "**** Pulling changes into Live [Hub's post-update hook]" > $LOG_FILE
echo "Starting at: `date`" >> $LOG_FILE

supervisorctl stop swd_`whoami`
echo `supervisorctl status swd_$ENVNAME` >> $LOG_FILE

if [ ! -d "$PROJECTDIR" ]; then
    echo "create virtualenv" >> $LOG_FILE
    virtualenv-3.2 $PROJECTDIR
fi

if [ -d $SOCKETDIR ]; then
    rm -rf $SOCKETDIR
    mkdir -p $SOCKETDIR/run
fi

cd $PROJECTDIR/$PROJECT || exit
CURRENT_REVISION=`git rev-parse HEAD`
echo "Last current revision $CURRENT_REVISION" >> $LOG_FILE

cd $PROJECTDIR
rm -rf $PROJECTDIR/$PROJECT
git clone -b `whoami` /home/`whoami`/git/`whoami`.swd.git $PROJECTDIR/$PROJECT

source $PROJECTDIR/bin/activate
$PROJECTDIR/bin/pip install -r $PROJECTDIR/$PROJECT/sport/fixtures/`whoami`.requirements.txt

cd $DJANGODIR

$PROJECTDIR/bin/python manage.py dumpdata > $WWWDIR/backup.json
$PROJECTDIR/bin/python manage.py collectstatic --clear --noinput
if [ $? -eq 1 ]; then
    rollback
fi
$PROJECTDIR/bin/python manage.py makemigrations
if [ $? -eq 1 ]; then
    rollback
fi
$PROJECTDIR/bin/python manage.py migrate auth
if [ $? -eq 1 ]; then
    rollback
fi
$PROJECTDIR/bin/python manage.py migrate
if [ $? -eq 1 ]; then
    rollback
fi

chmod +x $GUNICORN
supervisorctl start swd_`whoami`
ERROR_OCCURED=`supervisorctl status swd_$ENVNAME | grep 'STOPPED'`
echo "supervisor status : $ERROR_OCCURED" >> $LOG_FILE

# rollback if supervirsor start fail
if [ ! -z $ERROR_OCCURED ]; then
    echo "Supervisor is done but expected to start" >> $LOG_FILE
    rollback
fi

TIMESTAMP=date +"%T"
echo "[UPDATE]" > update.ini
echo "date=$TIMESTAMP" >> update.ini
echo "status=passed" >> update.ini

echo "Finish at: `date`" >> $LOG_FILE
exec git update-server-info
