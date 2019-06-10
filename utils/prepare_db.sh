#!/bin/sh

export PGPASSWORD=$DBPASS
psql -h $HOST -U $DBUSER -d $DBNAME -f /server/api/storage_module/config/db.sql