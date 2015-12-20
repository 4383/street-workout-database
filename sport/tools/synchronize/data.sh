#!/usr/bin/env bash

cd /home/production/projects/swd/
source /home/production/projects/swd/bin/activate
which python
cd /home/production/projects/swd/street-workout-database/sport/web
/home/production/projects/swd/bin/python /home/production/projects/swd/street-workout-database/sport/web/manage.py dumpdata > /home/production/www/swd/synchronize.json
deactivate

cp -R /home/production/www/swd/media /home/staging/www/swd/
chown -R staging:webuser /home/staging/www/swd/media

cd /home/staging/projects/swd/
source /home/staging/projects/swd/bin/activate
cd /home/staging/projects/swd/street-workout-database/sport/web
/home/staging/projects/swd/bin/python /home/production/projects/swd/street-workout-database/sport/web/manage.py loaddata /home/production/www/swd/synchronize.json
rm /home/production/www/swd/synchronize.json
deactivate




