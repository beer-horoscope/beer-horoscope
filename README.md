# The Modern Fortune Teller - Beer Horoscope

A fullstack, end-to-end implementation of an application which gives beer recommendations from a trained data model, from end-user input. 

![Architecture - Beer Recommendation System - scratch (5)](https://user-images.githubusercontent.com/61749/120901590-91e67a80-c601-11eb-88ea-a5ec7678912e.png)

# Pre-requisites

- An Openshift Cluster >= v4.7.x
- Beer Review Data (beer_reviews.csv)
    - [mirror 1](https://www.kaggle.com/rdoume/beerreviews) 
    - [mirror 2](https://data.world/socialmediadata/beeradvocate)

# Create Openshift Project

```bash
oc create new-project beer-rec-system
```

# Database Setup

## Create Database

```bash
# create mysq database deployment config
oc new-app mysql-persistent -p=NAMESPACE=openshift -p=DATABASE_SERVICE_NAME=mysql -p=MYSQL_DATABASE=beer_horoscope -p=MYSQL_USER=user -p=MYSQL_PASSWORD=password -p=MYSQL_ROOT_PASSWORD=password -p=MEMORY_LIMIT=8Gi -p=VOLUME_CAPACITY=5Gi -p=MYSQL_VERSION=8.0-el8

# create alias for the mysql pod
mpod=$(oc get pods --selector name=mysql --output name | awk -F/ '{print $NF}')

# copy over sql scripts
oc cp data ${mpod}:/tmp

# copy over beer review csv data (obtained in pre-requisite step)
oc cp /replace/with/path/to/beer_reviews.csv ${mpod}:/tmp/data

# create schema
oc exec $mpod -- bash -c "mysql --user=root < /tmp/data/01-schema.sql"

# load csv data (this will take a few minutes)
oc exec $mpod -- bash -c "mysql --user=root < /tmp/data/02-data-load.sql"

# create stored procs
oc exec $mpod -- bash -c "mysql --user=root < /tmp/data/03-store-procedures.sql"
```

## Validate Database

```bash
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
```

# Infrastructure

# Open Data Hub
