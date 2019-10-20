# Volume skill for Snips


## Installation with Sam

The easiest way to use this Action is to install it with [Sam](https://snips.gitbook.io/getting-started/installation)

`sam install actions -g https://github.com/gidocarper/snips-volume-control`

after the installation if it is not working try following commands:


**sudo usermod -a -G audio _snips-skills**

**sudo chmod +x /var/lib/snips/skills/snips-volume-control/action-volume-control.py**

**sudo systemctl restart snips-skill-server**

if that is still not working check with:

**amixer scontrols** 

which device you want to control and change line 14:

**m = alsaaudio.Mixer('Master')**

Master into the name of the device you are using to play sound.


and restart snips skills with

**sudo systemctl restart snips-skill-server**