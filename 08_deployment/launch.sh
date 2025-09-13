#!/usr/bin/env bash
set -e
IMAGE=mlflow-project
TAG=latest

docker build -t ${IMAGE}:${TAG} .

# --env-file injecte toutes les variables du .env dans le conteneur
docker run --rm -it \
  --env-file .env \
  -p 4000:${PORT:-7860} \
  ${IMAGE}:${TAG}
