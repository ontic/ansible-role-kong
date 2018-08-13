#!/bin/bash
# Copyright (c) Ontic. (http://www.ontic.com.au). All rights reserved.
# See the COPYING file bundled with this package for license details.

# Verify the installed location.
docker exec --tty ${container_id} env TERM=xterm which kong
# Verify the installed version.
docker exec --tty ${container_id} env TERM=xterm kong version
# Verify the health of services.
docker exec --tty ${container_id} env TERM=xterm kong health
# Expecting 401
docker exec --tty ${container_id} env TERM=xterm curl -i -X GET --url http://localhost:8000 --header "Host: example.com"
# Expecting 201
docker exec --tty ${container_id} env TERM=xterm curl -i -X POST --url http://localhost:8001/consumers/adam/key-auth/ --data "key=SECRET_KEY"
# Expecting 200
docker exec --tty ${container_id} env TERM=xterm curl -i -X GET --url http://localhost:8000 --header "Host: example.com" --header "apikey: SECRET_KEY"
