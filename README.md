[![Build Status](https://travis-ci.org/andela-jmwangi/bucketlist-api.svg?branch=master)](https://travis-ci.org/andela-jmwangi/bucketlist-api)
[![Coverage Status](https://coveralls.io/repos/github/andela-jmwangi/bucketlist-api/badge.svg?branch=master)](https://coveralls.io/github/andela-jmwangi/bucketlist-api?branch=master)

# Bucketlist API

Bucketlist API for an online Bucket List service using Flask.

# Features
The API offers the following features:

  1. User log in and register
  2. Listing, Creating, deleting and updating bucketlists.
  3. Creating, deleting and updating of bucketlist items.
  4. Token based authentication for API methods.
  5. Pagination for GET requests.
  4. Search by Bucketlist name.


# Usage

A sample request to create a single bucket list is as follows:

```
POST /api/v1/bucketlists/ HTTP/1.1
Host: localhost:5000
Content-Type: application/x-www-form-urlencoded
token: eyJhbGciOiJIUzI1NiIsImV4cCI6MzE0NjA2NDUwNjMsImlhdCI6MTQ2MDY0NTA2M30.eyJpZCI6OX0._c2r-kwCAbjV9GSHVV1Vw0k2cSSO1pFbnvfvw38BbFk
Cache-Control: no-cache
Postman-Token: 447971b2-9080-cb19-839e-2e0b82cc29b2

name=MyBucketList

{
    "created_by": 1,
    "date_created": "2016-04-15 04:12:35",
    "date_modified": "2016-04-15 04:12:37",
    "id": 26,
    "items": [],
    "name": "MyBucketList"
}
```

# Endpoints

| Endpoint                                  |Functionality                    |
|-------------------------------------------|---------------------------------|
| POST /auth/login                          | Logs a user in                  |
| POST /auth/register                       | Register a user                 |
| POST /bucketlists/                        | Create a new bucket list        |
| GET /bucketlists/                         | List all the created bucketlists|
| GET /bucketlists/<id>                     | Get single bucket list          |
| PUT /bucketlists/<id>                     | Update this bucket list         |
| DELETE /bucketlists/<id>                  | Delete this single bucket list  |
| POST /bucketlists/<id>/items/             | Create a new item in bucket list|
| PUT /bucketlists/<id>/items/<item_id>     | Update a bucket list item       |
| DELETE /bucketlists/<id>/items/<item_id>  | Delete an item in a bucket list |


# Set up

In the project root folder, follow the following instructions:

  1. Create a virtual environment by running the command `virtualenv env`.

  2. Activate the environment using the command `source env/bin/activate`.

  3. Run `pip install -r requirements.txt` to install all relevant dependencies.

  4. Run the command `python run.py` to start the server. The application will
  then be live at **http://localhost:5000/**

# Testing

In the project root folder, run command `nosetests`.

# Acknowledgements

This project is built using functionality from the following 3rd party libraries:

  1. [Flask](http://flask.pocoo.org/)
  2. [flask-restful](http://flask-restful-cn.readthedocs.org/en/0.3.4/)
  3. [flask-sqlalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
  4. [itsdangerous](http://pythonhosted.org/itsdangerous/)
  5. [marshmallow](https://marshmallow.readthedocs.org/en/latest/#)

# License

The MIT License

Copyright (c) 2016 Jack Mwangi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
