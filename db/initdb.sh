#!/bin/bash
set -e

export PGPASSWORD="$POSTGRES_PASSWORD"

# enable PostGIS
#psql -U $POSTGRES_USER $POSTGRES_DB -c "create extension postgis"
#psql -U $POSTGRES_USER $POSTGRES_DB -c "create extension postgis_topology"
#psql -U $POSTGRES_USER $POSTGRES_DB -c "create extension fuzzystrmatch"
#psql -U $POSTGRES_USER $POSTGRES_DB -c "create extension postgis_tiger_geocoder"


shp2pgsql -D -W latin1 -I -s 4326 /irisdata/iris-2013-01-01.shp geoiris | psql -U $POSTGRES_USER -d $POSTGRES_DB

psql -U $POSTGRES_USER $POSTGRES_DB -c "DELETE FROM geoiris WHERE gid IN (SELECT gid FROM (SELECT gid,RANK() OVER (PARTITION BY dcomiris ORDER BY gid) FROM geoiris) AS X WHERE X.rank > 1);"
