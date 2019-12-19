# Parent image
FROM mysql:5.6

LABEL description="HuBMAP MySQL 5.6 for UUID API Service" \
	version="1.0"

# Copy from host to image
COPY ./prod_dump_12_18.sql /docker-entrypoint-initdb.d/prod_dump_12_18.sql