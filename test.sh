#!/bin/sh

docker build -t s3 .

docker build -t s3c \
  --build-arg aws_id='changeme' \
  --build-arg aws_secret='changeme' \
  --build-arg aws_region='us-west-2' \
  configured-image/

DATA_CONTAINER_NAME="some-name"

docker run --rm --volumes-from $DATA_CONTAINER_NAME s3c --keep 1 -v /data/backups/ bucket.name $DATA_CONTAINER_NAME
