#!/bin/bash

PACKAGE_VERSION=$(grep '"tag":' docker.json | cut -d\" -f4)

IMAGE_NAME="748977760035.dkr.ecr.us-east-1.amazonaws.com/my-finance-backend:${PACKAGE_VERSION}"

docker build .. -t $IMAGE_NAME
