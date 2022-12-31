docker build -t ceph.api .
docker run -d -p 81:80 --name ceph.api --env-file .env -v ${PWD}:/app ceph.api