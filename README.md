# The Modern Fortune Teller - Beer Horoscope

A fullstack, end-to-end implementation of an application which gives beer recommendations from a trained data model, from end-user input. 

![Architecture - Beer Recommendation System - scratch (5)](https://user-images.githubusercontent.com/61749/120901590-91e67a80-c601-11eb-88ea-a5ec7678912e.png)

# Pre-requisites

- An Openshift Cluster >= v4.7.x
- Beer Review Data (beer_reviews.csv)
    - [mirror 1](https://www.kaggle.com/rdoume/beerreviews) 
    - [mirror 2](https://data.world/socialmediadata/beeradvocate)

# I. Create Openshift Project

```bash
oc create new-project beer-rec-system
```

# II. Database Setup

## Create Database

```bash
# create mysql database deployment config
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

# III. Infrastructure

## Option 1 - Use GitOps for Infrastructure Setup

### Install the "Red Hat GitOps Operator"

1. Goto the "Operatorhub"
2. Search for "OpenShift GitOps"
3. Select "Red Hat OpenShift GitOps"
4. Install for all namespaces
5. Wait until the operator is fully installed

### Open ArgoCD UI

1. Assign cluster admin role to the service account `openshift-gitops-argocd-application-controller`

```bash
oc adm policy add-cluster-role-to-user cluster-admin -z openshift-gitops-argocd-application-controller -n openshift-gitops
```

2. Obtain the admin password

```bash
oc -n openshift-gitops get secrets openshift-gitops-cluster -o 'go-template={{index .data "admin.password"}
}' | base64 -d

# example output: ZwCQrTRmgoLUpB1vdJ7I8sku5H9DPFyG%
# copy everything up to the '%' character
```

3. login to Argo CD: 
    - Uri: [https://openshift-gitops-server-openshift-gitops.apps.okd.thekeunster.local/](https://openshift-gitops-server-openshift-gitops.apps.okd.thekeunster.local/)
    - username: admin
    - password: obtained in previous step

4. Add a Git Repository to ArgoCD

    - click: ***Settings (Gear Icon)::Connect Repo Using Https*** 
    - fillin the form using the following git repository url: [
https://github.com/beer-horoscope/beer-horoscope.git](
https://github.com/beer-horoscope/beer-horoscope.git)
![Screenshot from 2021-06-08 02-39-22](https://user-images.githubusercontent.com/61749/121143551-c7a68180-c802-11eb-9a59-982c87c161a6.png)
## Option 2 - Use Script(s)

# IV. Open Data Hub

# V. Model Training

# VI. Application Walkthrough
