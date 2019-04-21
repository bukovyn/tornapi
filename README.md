<p align="center">
  <img src="https://github.com/bukovyn/tornapi/blob/master/static/img/tornapi.png" alt="tornapi" height="125">
  <br>
  <img src="https://img.shields.io/badge/python-3.*-blue.svg" alt="python -V">
  <a href="https://github.com/bukovyn/tornapi/pulls">
        <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="pull-requests">
    </a>
</p>

## :computer: Setup

```
git clone https://github.com/bukovyn/tornapi
```

### Database

We need a [MySQL](https://dev.mysql.com/doc/mysql-getting-started/en/) database in order for this API to have some data to work with. The simplest solution would be to have one set up locally.

I've included a SQL dump with some sample data in the [`sql`](https://github.com/bukovyn/tornapi/tree/master/sql) directory of this project. The [`config.py`](https://github.com/bukovyn/tornapi/blob/master/config.py) is preconfigured for this dump as root user with no password on local host and default sql port. Change according to your setup.

If you choose to use my sql dump file, create a database according to `config.py`. In our case its `university`
```
mysql
> create database university;
```

And finally to create the `students` table and fill it with the sample data, outside of the mysql shell run
```
mysql university < /tornapi/sql/students.sql
```


### API

Go into the repository directory and set up a [`virtualenv`](https://virtualenv.pypa.io/en/stable/)
```
virtualenv venv
```

Activate your environment
```
source venv/bin/activate
```

Install the required libraries
```
pip install -r requirements.txt
```

Run the API locally
```
python tornapi.py
```

By default, if hosted locally the API is accessible at `127.0.0.1:8000`

## :computer: How it works

This can be seen at the `/` endpoint but for a general idea, the API supports the `GET, POST, PUT, DELETE` methods through the content in the request body which must be in the form of  `content-type:application/json`

<p align="center">
  <img src="https://github.com/bukovyn/tornapi/blob/master/static/img/index.png" alt="index">
</p>

To query the table, send a `GET` to the endpoint which is the table name, in our students example that would be `127.0.0.1:8000/students`. To query a specific student send a `GET` to the `/students/{id}` endpoint. For instance, a student with the id `5` would be at `127.0.0.1:8000/students/5`.

This endpoint is dynamic and changes based on the name of your table. For example's sake, I used the students table.
