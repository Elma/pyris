FROM python:3.8-buster

ENV PYTHONUNBUFFERED 1

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get install wget ca-certificates
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get update -y
RUN apt-get install -y binutils libproj-dev gdal-bin postgresql-client-10 npm

RUN mkdir /app
WORKDIR /app

ADD setup.py /app/
ADD setup.cfg /app/
ADD README.md /app/README.rst
RUN python setup.py install

RUN npm install -g bower
ADD bower.json /app/
RUN bower install --allow-root

