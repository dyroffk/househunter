# Bungalow Tech Challenge -- HouseHunter

## Overview

Django application to ingest housing inventory details.

## Prequisites

Install Python dependencies with

```shell
pip install -r requirements.txt
```

## Ingesting data

Housing data can be imported via CSV by running

``` shell
./manage.py ingest inputfile.csv
```


## Runtime

Launch the development server with

``` shell
./manage.py runserver
```

## API Documentation

With the server running, Swagger API documentation can be found at: http://127.0.0.1:8000/swagger/
