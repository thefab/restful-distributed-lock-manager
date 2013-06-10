# API

## Concepts

Please read the [README.md](README.md) first (specifically the concepts section).

## Acquire a lock

### Request

    Method: POST
    Body (raw): {"title": "client title", "wait": 5, "lifetime": 300}
    URL: http://{hostname}:{port}/locks/{resource}

    {resource} must valid ([a-zA-Z0-9]+)

### Response

If the request is valid, it is blocking during a **maximum** of "wait" parameters (specified in the body of the request). Of course, the response is given as soon as the 
exclusive lock is available.

#### The lock is acquired

    StatusCode: 201 (Created)
    Header: Location: http://... 
        => (UNIQUE LOCK URL)
    Body: empty

#### The lock is not acquired (timeout)

    StatusCode: 408 (Request Timeout)
    Body: empty

#### The lock is not acquired (request deleted)

    StatusCode: 409 (Conflict)
    Body: empty

#### The request is invalid

    StatusCode: 400 (Bad Request)
    Body: error message
        => Bad body of the request

## Release a lock

### Request

    Method: DELETE
    URL: http://...
        => UNIQUE LOCK URL GOT IN THE LOCATION HEADER OF A SUCCESSFUL LOCK ACQUIRE REQUEST

### Response

#### The lock exist

    StatusCode: 204 (No Content)
    Body: empty
        => OK THE LOCK IS DELETED

#### The lock don't exist (lifetime expiration, bad url, already deleted...)

    StatusCode: 404 (Not Found)
    Body: error message

## Checking a lock (not really useful)

### Request

    Method: GET
    URL: http://...
        => UNIQUE LOCK URL GOT IN THE LOCATION HEADER OF A SUCCESSFUL LOCK ACQUIRE REQUEST

### Response

#### The lock exist

    StatusCode: 200 (OK)
    Header: Content-Type: application/hal+json

    Body (example): 
    {
        "uid": "aa4e181e17374148a21b30d9dcb941f9", 
        "title": "lock title", 
        "active_since": "2013-01-22T23:01:16.771799", 
        "_links": {
            "self": {
                "href": "/locks/foo/aa4e181e17374148a21b30d9dcb941f9"
            }, 
            "resource": {
                "href": "/resources/foo"
            }
        }, 
        "active_expires": "2013-01-22T23:06:16.771799", 
        "active": true, 
        "lifetime": 300, 
        "wait": 5
    }
    
        => THE BODY IS A VALID JSON/HAL OBJECT WITH SOME SELF DESCRIPTIVE PROPERTIES

#### The lock don't exist (lifetime expiration, bad url, already deleted...)

    StatusCode: 404 (Not Found)
    Body: error message

## Administrative request : delete all locks on a resource (active and waiting)

### Request

    Method: DELETE
    URL: http://{hostname}:{port}/resources/{resource}

    {resource} must valid ([a-zA-Z0-9]+)

### Response

#### There are some locks on the resource

    StatusCode: 204 (No Content)
    Body: empty
        => OK ALL LOCK ARE DELETED

#### There is no lock on the resource

    StatusCode: 404 (Not Found)
    Body: error message

#### You must provide an HTTP Basic authentication

    StatusCode: 401 (Unauthorized)

## Administrative request : delete all locks on all resources

### Request

    Method: DELETE
    URL: http://{hostname}:{port}/resources

### Response

#### There are some locks on the resource

    StatusCode: 204 (No Content)
    Body: empty
        => OK ALL LOCK ARE DELETED

#### You must provide an HTTP Basic authentication

    StatusCode: 401 (Unauthorized) 

## Administrative request : get all locks on a given resource 

### Request

    Method: GET
    URL: http://{hostname}:{port}/resources/{resource}

### Response

    StatusCode: 200 (OK)
    Header: Content-Type: application/hal+json

    Body (example): 
    {
        "_embedded": {
            "locks": [
            {
                "uid": "c97802647fcd4039a0563e48f9330d82",
                    "title": "lock title",
                    "active_since": "2013-02-18T22:58:12.785378",
                    "_links": {
                        "self": {
                            "href": "/locks/foo/c97802647fcd4039a0563e48f9330d82"
                        }
                    },
                    "active_expires": "2013-02-18T23:03:12.785378",
                    "active": true,
                    "lifetime": 300,
                    "wait": 10
            }
            ]
        },
        "_links": {
            "self": {
                "href": "/resources/bar"
            }
        },
        "name": "bar"
    }

        => THE BODY IS A VALID JSON/HAL OBJECT WITH SOME SELF DESCRIPTIVE PROPERTIES

## Administrative request : get all resources with locks

    Method: GET
    URL: http://{hostname}:{port}/resources

### Response

    StatusCode: 200 (OK)
    Header: Content-Type: application/hal+json

    Body (example):
    {
        "_embedded": {
            "resources": [
            {
                "_links": {
                    "self": {
                        "href": "/resources/foo"
                    }
                },
                "name": "foo"
            },
            {
                "_links": {
                    "self": {
                        "href": "/resources/bar"
                    }
                },
                "name": "bar"
            }
            ]
        },
        "_links": {
            "self": {
                "href": "/resources"
            }
        }
    }
    
    	=> THE BODY IS A VALID JSON/HAL OBJECT WITH SOME SELF DESCRIPTIVE PROPERTIES

## JSON/HAL

Have a look at [the JSON/HAL specification](http://stateless.co/hal_specification.html).
