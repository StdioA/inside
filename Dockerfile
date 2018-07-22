FROM daocloud.io/python:3-onbuild
# RUN mkdir -p /usr/src/app
# COPY . /usr/src/app
# WORKDIR /usr/src/app
ENV DJANGO_SETTINGS_MODULE inside.settings.docker
EXPOSE 8000
ENTRYPOINT [ "sh", "/usr/src/app/start-server.sh" ]
