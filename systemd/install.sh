#!/bin/bash

if [ $EUID != 0 ]; then
    echo "Please run as root"
    exit
fi

if [ ! -d "/etc/systemd/system" ]; then
	echo "/etc/systemd/system does not exist. Service cannot be installed."
	exit
fi

echo "Copying tm1628mpd.service to /etc/systemd/system..."
cp tm1628mpd.service /etc/systemd/system

echo "Enabling and starting service..."
systemctl daemon-reload
systemctl enable tm1628mpd.service
systemctl start tm1628mpd.service


