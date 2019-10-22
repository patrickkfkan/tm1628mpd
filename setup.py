import setuptools

setuptools.setup(
    name="tm1628mpd",
    version="0.0.1",
    author="Patrick Kan",
    author_email="patrickkfkan@gmail.com",
    description="Shows clock / MPD play time on TM1628 VFD 4-digit displays",
    long_description="",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: GPL 2.0",
    ],
    scripts=['bin/tm1628mpd'],
    install_requires=['python-mpd2','ioctl_opt'],
)
