# CHANGES

## Release 0.3

- python3 fixes
- smart shutdown with SIGINT or CONTROL + C

## Release 0.2

- the GET request on a resource URL returns always HTTP/200
- documentation update
- the GET request on a lock URL returns now a JSON/HAL resource
- python3 support
- admin requests
- light api change when acquiring lock (you can get an HTTP/409 if your waiting lock request is deleted by an admin request)

## Release 0.1 

- first release
