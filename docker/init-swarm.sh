#!/bin/bash

STACK_NAME="my-finance-backend"

echo "Spinning up 3 EC2 instances..."

for i in 1 2 3; do
  docker-machine create \
    --driver amazonec2 \
    --amazonec2-region us-east-1 \
    --amazonec2-root-size 8 \
    node-$i;
done


echo "Initializing Swarm mode..."

docker-machine ssh node-1 -- docker swarm init --advertise-addr $(docker-machine ip node-1)


echo "Adding the nodes to the Swarm..."

TOKEN=`docker-machine ssh node-1 docker swarm join-token worker | grep token | awk '{ print $5 }'`

for i in 2 3; do
  docker-machine ssh node-$i \
    -- docker swarm join --token ${TOKEN} $(docker-machine ip node-1):2377;
done


echo "Creating secret..."

eval $(docker-machine env node-1)
echo "foobar" | docker secret create secret_code -


echo "Deploying the Flask microservice..."

docker stack deploy --compose-file=docker-compose-swarm.yml ${STACK_NAME}


echo "Create the DB table and apply the seed..."

APP_NODE_LABEL="${STACK_NAME}_app"
NGINX_NODE_LABEL="${STACK_NAME}_nginx"

sleep 10
NODE=$(docker service ps -f "desired-state=running" --format "{{.Node}}" ${APP_NODE_LABEL})
eval $(docker-machine env $NODE)
CONTAINER_ID=$(docker ps --filter name=${APP_NODE_LABEL} --format "{{.ID}}")
docker container exec -it $CONTAINER_ID python manage.py db upgrade


echo "Get the IP address..."

sleep 10
eval $(docker-machine env node-1)
docker-machine ip $(docker service ps -f "desired-state=running" --format "{{.Node}}" ${NGINX_NODE_LABEL})
