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

After setting the .env file that includes required keys, you can use any database connection as follows:

```
query = "SELECT * FROM SAMPLE_TABLE LIMIT 1;"
with Vertica() as v:
    result = v.query(query)
```
