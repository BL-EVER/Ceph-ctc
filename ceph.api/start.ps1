docker build -t ceph.api .
docker run -d -p 81:81 --name ceph.api --env-file .env -v ${PWD}:/app ceph.api