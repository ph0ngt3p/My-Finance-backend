#!/bin/bash

IMAGE_NAME="registry.gitlab.com/tuandzung/my-finance:latest"

docker build .. -t $IMAGE_NAME
