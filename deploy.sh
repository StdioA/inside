#!/usr/bin/env bash

CurDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
Image="stdio/inside:v1"
ContainerName="inside_test"

build-img() {
  docker build -t ${Image} .
}

stop() {
  docker stop ${ContainerName}
  docker rm ${ContainerName}
}

start() {
  docker run --name ${ContainerName} --rm \
    -p 8000:8000 \
    -v ${CurDir}:/usr/src/app \
    ${Image}
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
