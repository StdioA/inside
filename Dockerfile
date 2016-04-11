FROM daocloud.io/python:2-onbuild
RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app
EXPOSE 8000
RUN sh ./deploy.sh
ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000"]
