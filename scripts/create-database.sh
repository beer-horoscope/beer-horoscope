#!/bin/bash

# create mysql database deployment config
oc new-app mysql-persistent -p=NAMESPACE=openshift -p=DATABASE_SERVICE_NAME=mysql -p=MYSQL_DATABASE=beer_horoscope -p=MYSQL_USER=user -p=MYSQL_PASSWORD=password -p=MYSQL_ROOT_PASSWORD=password -p=MEMORY_LIMIT=8Gi -p=VOLUME_CAPACITY=5Gi -p=MYSQL_VERSION=8.0-el8

# wait a minute until the deploy creates the mysql pod
sleep 30

# create alias for the mysql pod
mpod=$(oc get pods --selector name=mysql --output name | awk -F/ '{print $NF}')

# wait for the mysql pod to finish creating
kubectl wait --for=condition=Ready  --timeout=360s pod/$mpod

# copy over sql scripts
oc cp data ${mpod}:/tmp

# copy over beer data
wget https://github.com/beer-horoscope/beer-review-data-set/raw/main/beer_reviews_data.zip
unzip beer_reviews_data.zip
oc cp beer_reviews.csv ${mpod}:/tmp/data

# wait for database to go online
sleep 30

# create schema
oc exec $mpod -- bash -c "mysql --user=root < /tmp/data/01-schema.sql"

# load csv data (this will take a few minutes)
oc exec $mpod -- bash -c "mysql --user=root < /tmp/data/02-data-load.sql"

# create stored procs
oc exec $mpod -- bash -c "mysql --user=root < /tmp/data/03-store-procedures.sql"

# validate the database
oc exec $mpod -- bash -c "mysql --user=root -e 'show databases;'"

# validate database tables
oc exec $mpod -- bash -c "mysql --user=root -e 'use beer_horoscope; show tables;'"

# validate table columns
oc exec $mpod -- bash -c "mysql --user=root -e 'use beer_horoscope; describe beer_reviews;'"

# validate data load
oc exec $mpod -- bash -c "mysql --user=root -e 'use beer_horoscope; select count(*) from beer_reviews;'" 

# validate row data
oc exec $mpod -- bash -c "mysql --user=root -e 'use beer_horoscope; select * from beer_reviews limit 10;'"