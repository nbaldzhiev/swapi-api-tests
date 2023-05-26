#!/bin/bash

#
# The script has been developed and tested on MacOS Monterey 12.6, so there could be some differences with other OSs
# Usage:
#
# The script accepts one optional arguments:
#   - controls whether the container image is first built or not. Set it to False in order not to
#     build an image, i.e. ./test.sh False. Otherwise, an image would be built first.
#
# Examples:
#
# $ ./test.sh - Default. Builds the docker image
# $ ./test.sh False - Don't build an image
# # ./test.sh True - same as default ./test.sh - builds a docker image.
#

IMAGE_NAME='swapi-api-tests-image'
APP_NAME='swapi-api-tests-app'

if docker info ; then
  if [[ $1 != 'False' ]] ; then
    echo 'Starting the process of building a new docker image with the tests app...'
    docker build --tag $IMAGE_NAME .
    echo 'Successfully built the docker image!'
  fi
  docker run $IMAGE_NAME
  echo 'Ran the container in attached mode.'
else
  echo 'The command "docker info" was unsuccessful! Please either start or install Docker.'
fi