# Uploading/Copying files to Persistent Volume Mount

Goto the root of your local filesystem where your data model files are located. Files should look like the following: 

```bash
-rw-r--r--. 1 hershey hershey  20K Mar 22 23:52 beer_names_list.pickle
-rw-r--r--. 1 hershey hershey 6.8M Mar 22 23:52 corr.pickle
-rw-r--r--. 1 hershey hershey 618M Mar 22 23:52 cosine_sim.pickle
-rw-r--r--. 1 hershey hershey 619K Mar 22 23:52 dfbag.pickle
-rw-r--r--. 1 hershey hershey 198K Mar 22 23:52 indices.pickle
```

run the following:

```bash
oc cp . jumpbox:/mnt/storage/out
```


