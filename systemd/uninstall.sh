#!/bin/bash

if [ $EUID != 0 ]; then
    echo "Please run as root"
    exit
fi

echo "Stopping and disabling service..."
systemctl stop tm1628mpd.service
systemctl disable tm1628mpd.service
systemctl daemon-reload

if [ ! -f "/etc/systemd/system/tm1628mpd.service" ]; then
	echo "Warning: /etc/systemd/system/tm1628mpd.service does not exist."
else
	echo "Cleaning up files..."
	rm /etc/systemd/system/tm1628mpd.service
fi
