# tm1628mpd

A simple Python package that monitors the status of MPD running on devices with TM1628 4-digit VFD displays. When MPD is playing, it displays the time elapsed on the VFD. Otherwise, it displays the current time.

### Installation

```sh
$ git clone https://github.com/patrickkfkan/tm1628mpd.git
$ cd tm1628mpd
$ sudo pip install .
```

#### Running as a systemd service

To start tm1628mpd as a systemd service, continue from above:

```sh
$ cd systemd
$ sudo ./install.sh
```

You can restart, stop and check status of the service:

```sh
$ systemctl status tm1628mpd    # Check status
$ systemctl restart tm1628mpd   # Restart
$ systemctl stop tm1628mpd      # Stop
```

#### Running from console

If you do not use systemd, you can start tm1628mpd directly from the console:

```sh
$ sudo tm1628mpd
```

### Uninstallation

```sh
$ sudo pip uninstall tm1628mpd
```

If you installed tm1628mpd as a systemd service:

```sh
$ cd <path/to/tm1628mpd_installation>/systemd   # This is the same path where you ran the script to install the systemd service
$ sudo ./uninstall.sh
```


License
----
GPL 2.0

