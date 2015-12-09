#!/bin/sh
#
# An example hook script to prepare a packed repository for use over
# dumb transports.
#
# To enable this hook, rename this file to "post-update".

unset GIT_DIR
LOG_FILE="~/logs/swd/git.log"
PROJECT="street-workout-database"
PROJECTDIR=~/projects/swd
DJANGODIR=$PROJECTDIR/street-workout-database/sport/web
GUNICORN=$PROJECTDIR/$PROJECT/sport/tools/server/gunicorn/`whoami`.gunicorn.sh

echo "**** Pulling changes into Live [Hub's post-update hook]" >> $LOG_FILE
echo "Starting at: `date`" >> $LOG_FILE

if [ ! -d "$PROJECTDIR" ]; then
    virtualenv-3.2 $PROJECTDIR
    git clone -b release-v1.1 ~/git/swd.git $PROJECTDIR/$PROJECT
fi

cd $PROJECTDIR/$PROJECT || exit
git pull origin

source $PROJECTDIR/bin/activate
cd $DJANGODIR

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

chmod +x $GUNICORN
sh $GUNICORN

echo "Finish at: `date`" >> $LOG_FILE
exec git update-server-info
