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
PROJECTDIR=~/projects/swd
DJANGODIR=$PROJECTDIR/street-workout-database/sport/web
GUNICORN=$PROJECTDIR/$PROJECT/sport/tools/server/gunicorn/`whoami`.gunicorn.sh

echo "**** Pulling changes into Live [Hub's post-update hook]" >> $LOG_FILE
echo "Starting at: `date`" >> $LOG_FILE

if [ ! -d "$PROJECTDIR" ]; then
    virtualenv-3.2 $PROJECTDIR 2>> $LOGERROR_FILE
    git clone -b release-v1.1 ~/git/swd.git $PROJECTDIR/$PROJECT 2>> $LOGERROR_FILE
fi

cd $PROJECTDIR/$PROJECT || exit
git pull origin 2>> $LOGERROR_FILE

source $PROJECTDIR/bin/activate 2>> $LOGERROR_FILE
pip install -r $DJANGODIR/sport/fixtures/`whoami`.requirements.txt 2>> $LOGERROR_FILE

cd $DJANGODIR

python manage.py makemigrations 2>> $LOGERROR_FILE
python manage.py migrate 2>> $LOGERROR_FILE
python manage.py collectstatic 2>> $LOGERROR_FILE

chmod +x $GUNICORN
sh $GUNICORN 2>> $LOGERROR_FILE

echo "Finish at: `date`" >> $LOG_FILE
exec git update-server-info
