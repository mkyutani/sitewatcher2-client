#!/bin/env sh
#
#  Install sitewacher2-client
#

if [ $(id -u) -eq 0 ]; then
    # root
    SUDO=
else
    SUDO=sudo
fi

#
#  Build docker container
#
${SUDO} docker build . --tag sw2:latest

#
#  Schedule
#  (Cron.service must be running)
${SUDO} mkdir -p /var/log/sw2
${SUDO} crontab < schedule/crontab
${SUDO} cp -f schedule/sw2.cron.daily /etc
${SUDO} chmod +x /etc/sw2.cron.daily