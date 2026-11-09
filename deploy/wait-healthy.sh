#!/bin/bash
# Docker 18.09 / standalone Compose v1 equivalent of waiting for health.
set -eu
container="${1:-learncpp-demo-cupcake__webapp}"
attempt=0
while [ "$attempt" -lt 60 ]; do
    status=$(docker inspect --format '{{.State.Health.Status}}' "$container" 2>/dev/null) || {
        echo "Cannot inspect $container; check Docker access and docker-compose ps." >&2
        exit 1
    }
    if [ "$status" = healthy ]; then
        echo "$container is healthy"
        exit 0
    fi
    running=$(docker inspect --format '{{.State.Running}}' "$container")
    if [ "$status" = unhealthy ] || [ "$running" != true ]; then
        echo "$container failed health/startup checks ($status)." >&2
        docker logs --tail=50 "$container" >&2
        exit 1
    fi
    attempt=$((attempt + 1))
    sleep 2
done
echo "Timed out waiting for $container to become healthy." >&2
docker logs --tail=50 "$container" >&2
exit 1
