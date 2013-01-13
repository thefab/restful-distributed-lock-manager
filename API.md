# API

## Acquire a lock

### Request

    Method: POST
    Body (raw): {"title"; "client title", "wait": 5, "lifetime": 300}
    URL: http://{hostname}:{port}/locks/{resource}

    {resource} must valid ([a-zA-Z0-9]+)

### Response

If the request is valid, it is blocking during a **maximum** of "wait" parameters (specified in the body of the request). Of course, the response is given as soon as the 
exclusive lock is available. So, the "wait" parameters is a kind of timeout. 

#### The lock is acquired

    StatusCode: 201 (Created)
    Header: Location: http://... 
        => (UNIQUE LOCK URL)
    Body: empty

#### The lock is not acquired (timeout)

    StatusCode: 408 (Request Timeout)
    Body: empty

#### The lock is not acquired (request deleted by admin)

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
    Header: Content-Type: application/json
    Body: {"title"; "client title", "wait": 5, "lifetime": 300}
        => THE BODY IS A VALID JSON OBJECT WITH THREE PROPERTIES : title, wait, lifetime

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

#### You must provide an HTTP Basic authentification

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

#### You must provide an HTTP Basic authentification

    StatusCode: 401 (Unauthorized) 

    














