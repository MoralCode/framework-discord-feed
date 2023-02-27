#!/bin/bash
#https://unix.stackexchange.com/questions/22137/how-to-watch-rss-feed-for-new-entries-from-bash-script#22155

rsstail -i 3 -u https://frame.work/blog.rss -n 0 | while read x ; do play fail.ogg ; done

https://discord.com/api/webhooks/1050877441360531477/vE6rMxUOGhgYYZ35zMqxAgYWhKeEyONSJ99JV48gRo4S470KbzypJ6q6bbJ1eBRzgd9e