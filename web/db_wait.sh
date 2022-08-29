#!/bin/bash

echo "Waiting for postgres to be available."

while ! nc -z $sql_host $sql_port; do
	sleep 0.1
done

echo "Postgres available."

exec "$@"
