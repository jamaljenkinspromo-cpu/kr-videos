#!/bin/bash
# usage: dopart.sh NAME VIDEOID
set -e
cd ~/work/raw
N=$1; ID=$2
[ -s $N.mp4 ] || curl -sS -f -o $N.mp4 "https://resource2.heygen.ai/video/transcode/$ID/1080x1920.mp4"
ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets,has_b_frames,r_frame_rate -show_entries format=duration -of compact $N.mp4
ffmpeg -v error -y -i $N.mp4 -ac 1 -ar 16000 -c:a pcm_s16le $N.wav
python3 -c "import json;print(json.load(open('/root/work/build/blocks.json'))['$N'])" > $N.txt
