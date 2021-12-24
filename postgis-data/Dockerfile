FROM osgeo/gdal:ubuntu-small-3.4.0

RUN usermod -u 1000 www-data && groupmod -g 1000 www-data && \
        apt-get update

RUN apt-get install -y postgresql-client

COPY ["districts.geojson", "pscript.sql", "import-script.sh", "/postgis-data/"]

WORKDIR "/postgis-data"
