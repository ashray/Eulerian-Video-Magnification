#!/bin/bash
mkdir -p frames
mkdir -p output/iir output/butter

MAGNIFICATION=

function show_usage_and_exit {
	echo "usage: ./magnify-video.sh filter_type video_file [magnification]"
	echo "filter types: iir, ideal, butter"
	exit 1
}

function make_video {
	ffmpeg -framerate 30 -i frames/output_%d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4
}

function make_frames {
	python -u "$FILTER_TYPE.py" "input/$INPUT_VIDEO" $MAGNIFICATION
	# -u => unbuffered input and output
}

function clean_frames_folder {
	rm -rf frames
}

if [ -z "$1" ] || [ -z "$2" ]
then
	show_usage_and_exit
elif [ -z "$3" ]
then
	MAGNIFICATION=2
else
	MAGNIFICATION=$3
fi

FILTER_TYPE=$1
INPUT_VIDEO=$2

filename=$(basename "$INPUT_VIDEO")
extension="${filename##*.}"
filename="${filename%.*}"

#echo $filename
make_frames && make_video && clean_frames_folder
