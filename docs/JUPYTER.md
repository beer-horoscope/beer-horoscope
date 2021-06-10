# Setup Jupyter Notebooks

## I. Create a Jupyter Notebook Instance

- Goto the "Routes" section under the Project: `beer-rec-system` and click on the `jupyterhub` route. 
![Screenshot from 2021-06-10 01-13-13](https://user-images.githubusercontent.com/61749/121473999-10884280-c989-11eb-9dc8-f6f2444b4def.png)
- Clicking the link will lead to the Jupyterhub "Spawner Options" Page
    - Set JupyterHub Notebook Image: `s2i-scipy-notebook:v0.0.1`
    - Leave all other defaults and click "Start" and wait a few moments until Notebook creation completes. 

## II. Import Notebooks

- To import Notesbooks, on the main page, click the "upload" button and select all notebooks (i.e. *.ipynb files) located in your locally cloned repository, in the `src/models` directory. If all is well, then you should see something similar to the following: 
![Screenshot from 2021-06-10 01-25-14](https://user-images.githubusercontent.com/61749/121475205-ba1c0380-c98a-11eb-83f3-fed57986cfad.png)
- Once uploaded, you may open, view, and run the notebooks. 