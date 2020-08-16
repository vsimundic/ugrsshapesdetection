#!/bin/bash

if sudo chmod a+rw /dev/ttyUSB0
then
	python3 -m ugrsshapesdetection
fi
