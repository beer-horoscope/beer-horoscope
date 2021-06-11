# Model Training Walkthrough

This walkthrough will guide you setting up and training models on a local development machine

# Prerequisites

- MySql
    - [installation guide](https://dev.mysql.com/doc/refman/8.0/en/installing.html)
- python - v3.x
- pip - for python v3.x
- [virtualenv](https://virtualenv.pypa.io/en/latest/)
    - [installation guide](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv)

# Setup Database

Run the sql scripts found in the `data` folder in order. 

You have a few options on how to do this. 

***option 1***: Use the MySql Workbench GUI application

Execute the scripts in the GUI, one at a time in order

***option 2***: Use the `mysql` commandline interface tool

Execute the following commands: 

```bash
mysql -u root -p <you_root_password> > data/01-schema.sql
mysql -u root -p <you_root_password> > data/02-data-load.sql
mysql -u root -p <you_root_password> > data/03-store-procedures.sql
mysql -u root -p <you_root_password> > data/04-grants-permissions.sql
```

