# The Modern Fortune Teller - Beer Horoscope

A fullstack, end-to-end implementation of an application which gives beer recommendations from a trained data model, from end-user input. 

![Architecture - Beer Recommendation System - scratch (5)](https://user-images.githubusercontent.com/61749/120901590-91e67a80-c601-11eb-88ea-a5ec7678912e.png)

# Pre-requisites

- An Openshift Cluster >= v4.7.x

# I. Initial Setup

## 1. Create Openshift Project

```bash
oc create new-project beer-rec-system
```

## 2. Create Database

Obtain the Beer Review csv data from one of the mirrors in the prequisites section. Once obtained, place the csv file, "beer_reviews.csv", in the root of the repository folder. 

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

## 3. Validate Database

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

# II. Infrastructure

## Option 1 - Setup Infra with GitOps
---

## 1. Install the "Red Hat GitOps Operator"

1. Goto the "Operatorhub"
2. Search for "OpenShift GitOps"
3. Select "Red Hat OpenShift GitOps"
4. Install for all namespaces
5. Wait until the operator is fully installed

## 2. Create an ArgoCD Application

### i. Assign cluster admin role to the service account `openshift-gitops-argocd-application-controller`

```bash
oc adm policy add-cluster-role-to-user cluster-admin -z openshift-gitops-argocd-application-controller -n openshift-gitops
```

### ii. Obtain the admin password

```bash
oc -n openshift-gitops get secrets openshift-gitops-cluster -o 'go-template={{index .data "admin.password"}
}' | base64 -d

# example output: ZwCQrTRmgoLUpB1vdJ7I8sku5H9DPFyG%
# copy everything up to the '%' character
```

### iii. login to Argo CD: 
- Uri: [https://openshift-gitops-server-openshift-gitops.apps.okd.thekeunster.local/](https://openshift-gitops-server-openshift-gitops.apps.okd.thekeunster.local/)
- username: admin
- password: obtained in previous step

### iv. Add a Git Repository to ArgoCD
- click: ***Settings (Gear Icon)::Connect Repo Using Https*** 
- fill in the form field 
    - **repository url**: [
https://github.com/beer-horoscope/beer-horoscope.git](
https://github.com/beer-horoscope/beer-horoscope.git)
![Screenshot from 2021-06-08 02-39-22](https://user-images.githubusercontent.com/61749/121143551-c7a68180-c802-11eb-9a59-982c87c161a6.png)
- click: ***Connect***

### v. Add an Application to ArgoCD
- click: ***Applications (Stack Icon)::New App***
- fill in the form fields:
    - General 
        - ***Application Name***: beer-horoscope
        - ***Project***: default
        - ***Sync Policy***: Manual (Defaults)
        - ***Sync Options***: None (Defaults)
        - ***Prune Propogation Policy***: foreground
    - Source
        - ***Repository Url***: https://github.com/beer-horoscope/beer-horoscope.git
        - ***Revision***: HEAD
        - ***Path***: gitops
    - Destination
        - ***Cluster Url***: https://kubernetes.default.svc
        - ***Namespace***: beer-rec-system
    - Helm
        - ***Values File***: values.xml
        - ***spec.destination.server***: https://kubernetes.default.svc
![Screenshot from 2021-06-08 08-28-27](https://user-images.githubusercontent.com/61749/121194029-f7ba4880-c833-11eb-8438-5be1f712fc83.png)

### vi. Sync the Beer Horoscope Application
- click: ***Sync::Synchronize***, from the beer-horoscope application box and follow dialog respectively. This will bring in all sub applications tied via Helm Chart, as defined in the repository, and synchronize with your ArgoCD main application, beer-horoscope. 
- ***Before***:
![Screenshot from 2021-06-08 09-00-27](https://user-images.githubusercontent.com/61749/121215157-618f1e00-c845-11eb-9d1f-6871c87a4bfd.png)
- ***After***:
![Screenshot from 2021-06-08 11-35-51](https://user-images.githubusercontent.com/61749/121223976-b5056a00-c84d-11eb-95ba-35bb7dfbecf5.png)


## 3. Install Operators

## 4. Install Open Data Hub Instance

## 5. Install and Setup Kafka and Kafka Connect

## 6. Configure Storage

## 7. Deploy Applications

## Option 2 - Setup Infra with Script
---


# III. Open Data Hub

# IV. Model Training

# V. Application Walkthrough
