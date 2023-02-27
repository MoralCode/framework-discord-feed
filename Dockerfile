FROM alpine

RUN apk add rsstail

CMD bash ./rss.sh