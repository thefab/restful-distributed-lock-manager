1. To build docker image run:

```
    docker build -t stakater/restful-distributed-lock-manager .
```

2. To run the docker container:

```
    docker run -p 8888:8888 stakater/restful-distributed-lock-manager:latest
```