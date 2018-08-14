#!/bin/bash
# Copyright (c) Ontic. (http://www.ontic.com.au). All rights reserved.
# See the COPYING file bundled with this package for license details.

# Verify the installed location.
docker exec --tty ${container_id} env TERM=xterm which kong
# Verify the installed version.
docker exec --tty ${container_id} env TERM=xterm kong version
# Verify the health of services.
docker exec --tty ${container_id} env TERM=xterm kong health