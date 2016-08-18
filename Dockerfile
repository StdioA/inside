FROM daocloud.io/python:3-onbuild
ENV DJANGO_SETTINGS_MODULE inside.settings.docker
EXPOSE 8000
ENTRYPOINT [ "bash", "/usr/src/app/start-server.sh" ]
