#!/bin/bash
set -e
echo "Starting rsyslog"
service rsyslog start
echo "Starting dbus"
service dbus start
echo "Starting avahi daemon"
avahi-daemon --no-drop-root --daemonize --syslog --debug
tail -f /var/log/daemon.log &
gunicorn api:app --reload --bind 0.0.0.0
