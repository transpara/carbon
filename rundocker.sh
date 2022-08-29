docker run --rm -d \
    --pid host \
    --network transpara \
    --name carbon \
    --hostname carbon \
    -e host_name=`hostname` \
    -e PYTHONUNBUFFERED=1 \
    -e promURL="http://tstore-api:80/api/v1/write" \
    transpara/carbon
