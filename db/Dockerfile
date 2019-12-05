FROM geelweb/postgis:10

RUN apt-get update -y
RUN apt-get install -y wget unzip postgis

RUN mkdir /irisdata
WORKDIR /irisdata

RUN wget https://www.data.gouv.fr/s/resources/contour-des-iris-insee-tout-en-un/20150428-161348/iris-2013-01-01.zip
RUN unzip /irisdata/iris-2013-01-01.zip

COPY initdb.sh /docker-entrypoint-initdb.d/z-initdb.sh
