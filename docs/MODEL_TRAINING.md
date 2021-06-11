# Model Training Walkthrough

This walkthrough will guide you through setting up and training models on a local development machine

# Prerequisites

- MySql
    - [installation guide](https://dev.mysql.com/doc/refman/8.0/en/installing.html)
- python - v3.x
- pip - for python v3.x
- [virtualenv](https://virtualenv.pypa.io/en/latest/)
    - [installation guide](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv)

# I. Setup Database

## i. Obtain a Data Set

1. A data set can be obtained [here](https://github.com/beer-horoscope/beer-review-data-set/raw/main/beer_reviews_data.zip)

2. Unzip the archive and note the location. For this walkthrough we will denote the location as `/tmp/data/beer_reviews.csv`

## ii. Prep and Run Scripts

1. Update the script file `data/02-data-load.sql`, and update the `LOAD DATA LOCAL INFILE` path as noted in the previous section. i.e. `LOAD DATA LOCAL INFILE /tmp/data/beer_reviews.csv` 

2. Run the sql scripts found in the `data` folder in order. 

    You have a few options on how to do this. 

    ***option 1***: Use the MySql Workbench GUI application

    Execute the scripts in the GUI, one at a time in order

    ***option 2***: Use the `mysql` commandline interface tool

    Execute the following commands: 

    ```bash
    # NOTE: no spaces between parameter and parameter values -u and -p

    mysql -uroot -p<your_root_password> > data/01-schema.sql
    mysql --local-infile=1 -uroot -p<you_root_password> > data/02-data-load.sql
    mysql -uroot -p<your_root_password> > data/03-store-procedures.sql
    mysql -uroot -p<your_root_password> > data/04-grants-permissions.sql
    ```

# II. Train Data Model

## i. Setup Dev Environment Script

1. Open the file: `scripts/train-models-local.sh`.

2. Update all values in the script to match your environment

## ii. Train Models

To begin training models run the following: 

```bash
source data/train-models-local.sh
```



