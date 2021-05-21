
# Messages API


![GitHub repo size](https://img.shields.io/github/license/michal-siedlecki/messages-api)
![GitHub repo size](https://img.shields.io/github/repo-size/michal-siedlecki/messages-api)


The task is to design an API and create an application for saving and returning
saved and edited short texts (up to 160 characters).
The solution to the task is to be an API that is easy to use by other applications.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed `python` >= 3.6.2
* You have a `<Windows/Linux/Mac>` machine.

## Installing Messages API

To install Messages API, follow these steps:

Linux and macOS activate virtual environment and install dependencies:
```
git clone https://github.com/michal-siedlecki/messages-api
source venv/bin/activate
pip install -r requirements.txt
```
Then export app settings to evironmental variables (choose one of config settings from `config.py`)
```
export APP_SETTINGS="config.DevelopmentConfig"
```

Create two Postgres databases. Name it : `messages` for development  and `messages_testing` and for testing:
```
$ psql
# create database messages;
CREATE DATABASE
# create database messages_testing;
CREATE DATABASE
# \q
```
Then export development database URI to evironmental variables
```
export DATABASE_URL="postgresql:///messages"
```

Now You can run prepared migrations to populate database:
```
python manage.py db upgrade
```
In order to run Messages API application type:

```
flask run
```



## Using Messages API

To use Messages API type:

```
flask run
```

Now app is available under localhost:8000.
`POST | PATCH | DELETE` Theise methods require authentication. The authentication token can be set in evironmental variable by typing:
```
export TOKEN='token'
```  
Since it is API type application below is the description of requests:


## Get application info

### Request

`GET /`

    curl -i -H 'Accept: application/json' http://localhost:5000/

### Response

    HTTP/1.0 200 OK
	Content-Type: application/json
	Content-Length: 109
	Server: Werkzeug/2.0.1 Python/3.6.9
	Date: Fri, 21 May 2021 14:54:40 GMT
	
    {
	    App name: "Messages API",
	    links: 
		    {
			    items: "http://127.0.0.1:5000/api/v1",
				self: "http://127.0.0.1:5000/"
			}
	}
	
## Create a new message

### Request

`POST /api/v1/messages`

    curl -i -H 'Accept: application/json' -d 'content=Hello&password=token' http://localhost:5000/api/v1/messages

### Response

    HTTP/1.0 201 CREATED
	Content-Type: application/json
	Content-Length: 35
	Server: Werkzeug/2.0.1 Python/3.6.9
	Date: Fri, 21 May 2021 15:54:40 GMT

    [
        {
            "content":"Hello World",
            "id":1
        }
    ]
    
## Get all messages

### Request

`GET /api/v1/messages`

    curl -i -H 'Accept: application/json' http://localhost:5000/api/v1/messages

### Response

   
    HTTP/1.0 200 OK
	Content-Type: application/json
	Content-Length: 35
	Server: Werkzeug/2.0.1 Python/3.6.9
	Date: Fri, 21 May 2021 15:55:40 GMT

    [
        {
            "content":"Hello World",
            "id":1
        }
    ]


## Get a detail messages view

### Request

`GET /messages/id`

    curl -i -H 'Accept: application/json' http://localhost:5000/api/v1/messages/1

### Response

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 43
    Server: Werkzeug/2.0.1 Python/3.6.9
    Date: Fri, 21 May 2021 15:34:20 GMT

    {"content":"Hello World","id":1,"views":3}

## Get a non-existent message

### Request

`GET /message/non-existing-id`

    curl -i -H 'Accept: application/json' http://localhost:5000/messages/9999

### Response

    HTTP/1.0 404 NOT FOUND
    Content-Type: application/json
    Content-Length: 91
    Server: Werkzeug/2.0.1 Python/3.6.9
    Date: Fri, 21 May 2021 15:36:23 GMT

    {
        "code":404,
        "description":"Not found the resource with requested URL.",
        "name":"Not found"
    }

## Update message

### Request

`PATCH /messages/id`

    curl -i -H 'Accept: application/json' -d 'content=Welcome&password=token' http://localhost:5000/api/v1/messages/1


### Response

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 39
    Server: Werkzeug/2.0.1 Python/3.6.9
    Date: Fri, 21 May 2021 15:36:23 GMT

    {
        "content":"Welcome",
        "id":1,
        "views":1
    }

## Delete message

### Request

`DELETE /messages/id`

    curl -i -H 'Accept: application/json' -d 'password=token' http://localhost:5000/api/v1/messages/1


### Response

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 3
    Server: Werkzeug/2.0.1 Python/3.6.9
    Date: Fri, 21 May 2021 16:36:23 GMT

    [ ]


## Attempt to create a message using wrong token

### Request

`POST /messages/`

    curl -i -H 'Accept: application/json' -X POST -d 'password=oops' http://localhost:5000/api/v1/messages

### Response

    HTTP/1.0 403 FORBIDDEN
    Content-Type: application/json
    Content-Length: 111
    Server: Werkzeug/2.0.1 Python/3.6.9
    Date: Fri, 21 May 2021 16:46:23 GMT

    {
    "code": 403,
    "description": "Unauthorized users cannot create, update or delete messages",
    "name": "Unauthorized"
    }



## Contributors

Thanks to the following people who have contributed to this project:

* [@michal-siedlecki](https://github.com/michal-siedlecki) 😎 [author]


## Contact

If you want to contact me you can reach me at <siedlecki.michal@gmail.com>.

## License

This project uses the following license: MIT (<https://github.com/michal-siedlecki/messages-api/blob/main/LICENSE>).


