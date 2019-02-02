This is the home for the routing service.

Use python 3.6+


**ENSURE YOU KILL THIS SERVICE WHEN NOT IN USE**

To start, create a cron job:
$ crontab -e
(For mojave, you may need to use
$ EDITOR=/usr/bin/vim crontab -e
)
(you should now be in a vim text editor)
enter the following:
*/5 * * * * python3 /path/to/dist/route/route_main.py

(this will run the service every 5 minutes.. 1:05, 1:10, 1:15, ..)
