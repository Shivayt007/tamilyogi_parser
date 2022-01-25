# tamilyogi Parser
## parse_tamilyogi.py
This scrit python allows to parse and dawnload last 5 movies added in the site web.
By default:
* The movie dawnload path is __/opt__
* The tmp file path is __/opt__
* The number of latest movies to parse during each play is 5

You can change those default variables in argumet:
- path (movie dawnload path)
- tmp_path (tmp file path)
- number (number of latest movies to parse)

__Ex:__ 
__python /opt/scrpits/parse_tamilyogi.py -path '/opt/movies' -tmp_path '/opt/log' -number 5__
----------------
## schedule.sh
Ths script shell allows to automatize your script python on Linux using crontab.
__to add in crontab__
*run each 4 hours*
1. Change line 29 in schedule.sh as you want
2. edit corntab
__crontab -e__
3. add line to run script bash each 4 hours and get a log file 
__0 */4 * * * bash /opt/scrpits/schedule.sh >> /opt/log/parse_tamilyogi.log__
4. Reload crontab
__/etc/init.d/cron reload__
