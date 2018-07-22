#!/usr/bin/env bash

CurDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
Image="stdioa/inside:v1"
ContainerName="inside_container"

build-img() {
  docker build -t ${Image} .
}

stop() {
  docker stop ${ContainerName}
  docker rm ${ContainerName}
}

start() {
  docker run --name ${ContainerName} -d \
    -p 8000:8000 \
    -v ${CurDir}:/usr/src/app \
    ${Image}
    # -v /$(pwd):/usr/src/app \
}

reload() {
  docker exec ${ContainerName} python manage.py migrate
  docker kill -s HUP ${ContainerName}
}

Action=$1

shift

case "$Action" in
  build-img) build-img "$@";;
  # release-img) release-img "$@";;
  start) start "$@";;
  stop) stop ;;
  reload) reload "$@" ;;
  restart)
    stop
    start
    ;;
  shell) shell ;;
  test) test "$@" ;;
  *)
    echo "Usage:"
    echo "$0 start|stop|restart"
    echo "$0 reload [full]"
    echo "$0 build-img"
    # echo "$0 release-img"
    exit 1
    ;;
esac

exit 0
