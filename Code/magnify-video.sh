#!/bin/bash
rm -f magnified.mp4
python driver.py $1
avconv -i frames/output_%d.png -r 30 -b 65536k magnified.mp4