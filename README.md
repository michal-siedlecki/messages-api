
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


## Using Messages API

In order to use Messages API type:

```
flask run
```

Now app is available under localhost:8000.
`POST | PATCH | DELETE` Theise methods require authentication. The authentication token can be set in evironmental variable by typing:
```
export TOKEN='token'
``` 

## Application demo:

- Get all messages:
http://messages-app-pl.herokuapp.com/api/v1/messages/
- Get message detail:
http://messages-app-pl.herokuapp.com/api/v1/messages/1

# Requests description
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

`GET /api/v1/messages/id`

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

`GET /api/v1/messages/non-existing-id`

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

`PATCH /api/v1/messages/id`

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

`DELETE /api/v1/messages/id`

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

`POST /api/v1/messages/`

    curl -i -H 'Accept: application/json' -X POST -d 'content=Hi&password=oops' http://localhost:5000/api/v1/messages

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


## Attempt to create a message with too long content

### Request

`POST /api/v1/messages/`

    curl -i -H 'Accept: application/json' -d 'content=Moscow shows off its military hardware at the top of the world as the race for resources increases tensions between Russia and NATOMoscow shows off its military hardware at the top of the world as the race for resources increases tensions between Russia and NATO allies&password=token' http://localhost:5000/api/v1/messages


### Response

    HTTP/1.0 413 REQUEST ENTITY TOO LARGE
    Content-Type: application/json
    Content-Length: 90
    Server: Werkzeug/2.0.1 Python/3.6.9
    Date: Fri, 21 May 2021 16:46:23 GMT

    {
    "code": 413,
    "description": "The maximum content length is 160",
    "name": "Payload Too Large"
    }


## Tests

Several unit tests have been prepared for the application. To run the tests type:
````buildoutcfg
python tests.py
````


## Deployment

Messages API is deployed on Heroku Cloud Application using Heroku CLI. It is installed by:
```buildoutcfg
curl https://cli-assets.heroku.com/install.sh | sh
```

After installation You can login into CLI and create application:
```buildoutcfg
heroku login

heroku create messages-example-app
````

Since application was created using git version control it has to be pushed using command:
````buildoutcfg
git push heroku master
````
After that it's needed to set environmental variables using Heroku app settings in heroku dashboard.
Then set up the database:
```buildoutcfg
heroku addons:create heroku-postgresql:hobby-dev --app messages-example-app
```
You can see that since this moment Heroku set `DATABASE_URL` environmental variable to a value. Using migrations populate database with tables.
```buildoutcfg
heroku run python manage.py db upgrade --app messages-example-app
```
Applicaiton is deployed. 
Now when there is need to change You have to push it on Heroku:
```buildoutcfg
git push heroku master
```

## Contact

* [@michal-siedlecki](https://github.com/michal-siedlecki) 😎 [author]

If you want to contact me you can reach me at <siedlecki.michal@gmail.com>.

## License

This project uses the following license: MIT (<https://github.com/michal-siedlecki/messages-api/blob/master/LICENSE>).


