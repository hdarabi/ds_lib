# Data Science Library

This aim of this package is a to automate and simplify repetitive data science tasks.

# Installation Guide

Run the following commands

```
git clone https://github.com/hdarabi/ds_lib.git .
cd ds_lib
python setup.py install
```

# Using Database Connection

After setting the .env file that includes required keys
```
from dotenv import load_dotenv
load_dotenv()
```

you can use any database connection as follows:


```
query = "SELECT * FROM SAMPLE_TABLE LIMIT 1;"
with Vertica() as v:
    result = v.query(query)
```

# Installing Updates
After activating the target virtual environment, go to the git folder of 
the ds_lib and pull the latest changes. Running the below command 
automatically installs the latest version of the library.

```
sudo python setup.py install
```