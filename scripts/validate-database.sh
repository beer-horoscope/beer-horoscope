#!/bin/bash

# create alias for the mysql pod
mpod=$(oc get pods --selector name=mysql --output name | awk -F/ '{print $NF}')

# validate the database
echo "------------------------"
echo "1: validate the database"
echo "------------------------"

oc exec $mpod -- bash -c "mysql --user=root -e 'show databases;'"

# validate database tables
echo "---------------------------"
echo "2: validate database tables"
echo "---------------------------"

oc exec $mpod -- bash -c "mysql --user=root -e 'use beer_horoscope; show tables;'"

# validate table columns
echo "---------------------------"
echo "3: validate table columns"
echo "---------------------------"

oc exec $mpod -- bash -c "mysql --user=root -e 'use beer_horoscope; describe beer_reviews;'"

# validate data load
echo "---------------------------"
echo "4: validate data load"
echo "---------------------------"

oc exec $mpod -- bash -c "mysql --user=root -e 'use beer_horoscope; select count(*) from beer_reviews;'" 

# validate row data
echo "---------------------------"
echo "5: validate row data"
echo "---------------------------"

oc exec $mpod -- bash -c "mysql --user=root -e 'use beer_horoscope; select * from beer_reviews limit 10;'"