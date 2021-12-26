#!/usr/bin/bash

cd /postgis-data|| echo "Directory Not Found"
export PGPASSWORD="$POSTGRES_PASSWORD"; psql -U "$POSTGRES_USER" -h postgres -d "$POSTGRES_DB" -f pscript.sql
ogr2ogr --debug ON -f PostgreSQL PG:"host=postgres port=5432 user=$POSTGRES_USER dbname=$POSTGRES_DB password=$POSTGRES_PASSWORD" -update -overwrite -select name,name:en -lco GEOMETRY_NAME=geometry -lco FID=gid -nln districts districts.geojson