#!/bin/bash
IMAGE_NAME=core-service-lib

docker run -p 5000:5000 --rm -it \
    -v /etc/localtime:/etc/localtime:ro \
    -v /etc/timezone:/etc/timezone:ro \
    ${IMAGE_NAME}:local
