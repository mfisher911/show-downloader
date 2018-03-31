#!/bin/sh

recording=$(ls ~/show-downloader/"$(date +%F)"*.mp3)
open -a /Applications/Audacity/Audacity.app $recording
