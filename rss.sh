#!/bin/bash
#https://unix.stackexchange.com/questions/22137/how-to-watch-rss-feed-for-new-entries-from-bash-script#22155

rsstail -i 3 -u example.com/rss.xml -n 0 | while read x ; do play fail.ogg ; done