#!/bin/bash

# set project
oc project beer-rec-system

# remove mysql template instance and artifacts
oc delete deploymentconfig mysql
oc delete secret mysql
oc delete service mysql
oc delete pvc mysql

rm beer_reviews_data.zip
rm beer_reviews.csv