# Infrastructure, Deployment, and Setup

## I. Create Openshift Project

```bash
oc create new-project beer-rec-system
```

## II. Install the "Red Hat GitOps Operator"

1. Goto the "Operatorhub"
2. Search for "OpenShift GitOps"
3. Select "Red Hat OpenShift GitOps"
4. Install for all namespaces
5. Wait until the operator is fully installed

## III. Create an ArgoCD Application

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
- Uri: 
    - ***option 1***: click on the Openshift Application "OpenShift GitOps": 
    ![Screenshot from 2021-06-09 17-55-21](https://user-images.githubusercontent.com/61749/121439611-e2d0d880-c94b-11eb-8a61-b5e73405ee68.png)

    - ***option 2***: use the terminal to get the uri
    ```bash
    #get the argocd route uri
    argocd_uri=$(oc get routes openshift-gitops-server -n openshift-gitops -o 'jsonpath={.spec.host}')
    
    # print the full uri and navigate to that in your browser
    # example: https://openshift-gitops-server-openshift-gitops.apps.cluster.local
    echo https://$argocd_uri
    ```
     
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
- click: ***Sync::Synchronize***, from the beer-horoscope application box and the following modal dialog respectively. This will bring in all sub applications tied via Helm Chart, as defined in the repository, and synchronize with your ArgoCD main application, beer-horoscope.

- ***Before***:
![Screenshot from 2021-06-08 09-00-27](https://user-images.githubusercontent.com/61749/121215157-618f1e00-c845-11eb-9d1f-6871c87a4bfd.png)

- ***After***:
![Screenshot from 2021-06-09 13-25-43](https://user-images.githubusercontent.com/61749/121408647-40522e80-c926-11eb-9772-547a24090408.png)

## IV. Install Operators

- click: on the `00-operators` Application Tile and you will be presented with the following application layout: 
![Screenshot from 2021-06-09 14-09-31](https://user-images.githubusercontent.com/61749/121414518-55ca5700-c92c-11eb-807d-1b8672f430b1.png)
- click: ***Sync::Synchronize***, from the `00-operators` application box and the following modal dialog respectively. This will deploy the Red Hat AMQ Streams and Open Data Hub Operator into your cluster. 
- Validate the deployment: 
    - The ArgoCD application details should look similar to the following: 
    ![Screenshot from 2021-06-09 14-17-16](https://user-images.githubusercontent.com/61749/121415500-6af3b580-c92d-11eb-8c3f-130a0d765e17.png)
    - Review your installed operators in your project within Openshift. 
    ![Screenshot from 2021-06-09 14-18-20](https://user-images.githubusercontent.com/61749/121415629-91b1ec00-c92d-11eb-9889-9af8815d9f7f.png)

## V. Install a MySql Database Instance

- click: on the `01-database` Application Tile and you will be presented with the following application layout: 
![Screenshot from 2021-06-09 14-31-47](https://user-images.githubusercontent.com/61749/121417370-7051ff80-c92f-11eb-94ce-f98e1543ef5d.png)
- click: ***Sync::Synchronize***, from the `01-database` application box and the following modal dialog respectively. This will deploy a Persistent MySql Database instance leveraging an Openshift Template. 
- Validate the deployment: 
    - The ArgoCD application details should look similar to the following: 
    ![Screenshot from 2021-06-09 14-41-44](https://user-images.githubusercontent.com/61749/121418708-d8551580-c930-11eb-95e8-ee8b343f358b.png)
    - Validate the deployment topology in "Developer" mode:
    ![Screenshot from 2021-06-09 14-55-10](https://user-images.githubusercontent.com/61749/121420459-b78dbf80-c932-11eb-9e9b-521073cf2981.png)
    - Validate the database schema, tables, and data at a command line terminal
        ```bash
        # make sure the correct openshift project is selected
        oc project beer-rec-system

        # run the validation script from the root of the source repository w/in a bash shell
        source scripts/validate-database.sh
        ```

## VI. Install Open Data Hub Instance

- click: on the `02-odh` Application Tile and you will be presented with the following application layout: 
![Screenshot from 2021-06-09 15-19-54](https://user-images.githubusercontent.com/61749/121423710-2d475a80-c936-11eb-80ba-c0378227e2b8.png)
- click: ***Sync::Synchronize***, from the `02-odh` application box and the following modal dialog respectively. This will deploy Kubeflow artifacts as defined in the KfDef file: `infra/02-odh/odh-kfedf-data-catalog.yaml`. For this instance, an instance of Jupyter Hub will be deployed and accessible via a Route.  
- Validate the deployment: 
    - The ArgoCD application details should look similar to the following: 
    ![Screenshot from 2021-06-09 15-25-58](https://user-images.githubusercontent.com/61749/121424500-03426800-c937-11eb-87af-18e0c5921f78.png)
    - Validate the service routes for the Open Data Hub Dashboard and Jupyter Hub by navigating to the "Routes" section in Openshift. You should see two valid routes.
    ![Screenshot from 2021-06-09 15-29-16](https://user-images.githubusercontent.com/61749/121424913-78ae3880-c937-11eb-8835-4d82f6b84392.png)

## VII. Install and Setup Kafka and Kafka Connect

- click: on the `03-kafka` Application Tile and you will be presented with the following application layout: 
![Screenshot from 2021-06-09 19-14-10](https://user-images.githubusercontent.com/61749/121445372-ef0e6300-c956-11eb-84f8-71bb29f25ea2.png)
- click: ***Sync::Synchronize***, from the `03-kafka` application box and the following modal dialog respectively. This will deploy a Kafka Cluster, Topics, Kafka Connect Cluster, and Kafka Connectors. 
- Validate the deployment: 
    - The ArgoCD application details should look similar to the following: 
    ![Screenshot from 2021-06-09 19-27-38](https://user-images.githubusercontent.com/61749/121446289-c9825900-c958-11eb-88da-e83571a62c41.png)
    - Validations at the terminal
    ```bash
    # check available connectors
    oc exec -i `oc get pods --field-selector status.phase=Running -l strimzi.io/name=my-connect-cluster-connect -o=jsonpath='{.items[0].metadata.name}'` -- curl -s http://my-connect-cluster-connect-api:8083/connector-plugins | jq

    # check connector status - debezium-mysql-kafka-connector
    oc exec -i `oc get pods --field-selector status.phase=Running -l strimzi.io/name=my-connect-cluster-connect -o=jsonpath='{.items[0].metadata.name}'` -- curl -s http://my-connect-cluster-connect-api:8083/connectors/debezium-mysql-kafka-connector/status | jq 

    # check connector status - http-sink-connector
    oc exec -i `oc get pods --field-selector status.phase=Running -l strimzi.io/name=my-connect-cluster-connect -o=jsonpath='{.items[0].metadata.name}'` -- curl -s http://my-connect-cluster-connect-api:8083/connectors/http-sink-connector/status | jq 

    # list kafka topics
    oc exec -i `oc get pods --field-selector status.phase=Running -l strimzi.io/name=my-connect-cluster-connect -o=jsonpath='{.items[0].metadata.name}'` -- bin/kafka-topics.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --list
    ```
## VIII. Configure Storage

- click: on the `04-storage` Application Tile and you will be presented with the following application layout: 
![Screenshot from 2021-06-09 19-52-48](https://user-images.githubusercontent.com/61749/121447926-4d8a1000-c95c-11eb-800a-648941971426.png)
- click: ***Sync::Synchronize***, from the `04-storage` application box and the following modal dialog respectively. This will deploy a 100Gi persistent volume claim, which will be used to store trained model data. 
- Validate the deployment: 
    - The ArgoCD application details should look similar to the following: 
    ![Screenshot from 2021-06-09 19-55-39](https://user-images.githubusercontent.com/61749/121448157-b1143d80-c95c-11eb-88b9-f6f602b45f13.png)


## IX. Deploy Applications

- click: on the `04-storage` Application Tile and you will be presented with the following application layout: 
![Screenshot from 2021-06-09 23-59-00](https://user-images.githubusercontent.com/61749/121467441-aff40800-c97e-11eb-8681-f00d7c1197d1.png)
