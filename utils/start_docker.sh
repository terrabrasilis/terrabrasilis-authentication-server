#!/bin/bash

docker run -p 8000:8000 --name auth-api-server --rm \
--env HOST=localhost --env PORT=port --env DBNAME=database --env DBUSER=user --env DBPASS=password \
-d auth-api-server:v1
