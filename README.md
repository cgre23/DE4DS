![O'Reilly home](https://cdn.oreillystatic.com/images/sitewide-headers/oreilly_logo_mark_red.svg)



### Data Engineering for Data Scientists

Materials for the Live Online Training

Presented by Max Humber on November 12, 2020



#### Install

```sh
pip install sklearn-pandas
pip install fire
pip install rollbar
pip install python-dotenv
pip install apache-airflow
pip install gazpacho, rich
```

set Airflow directory: export AIRFLOW_HOME=`pwd`/airflow
airflow initdb
airflow test football fetch "2020-11-12"
airflow webserver -p 8080
go to localhost:8080
airflow scheduler

ALTERNATIVE for scheduling using hickory
pip install hickory
